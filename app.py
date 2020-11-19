"""
    Copyright 2020 Lucas Bernard Black

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# static data
months = {
    "Jan": 0,
    "Feb": 1,
    "Mar": 2,
    "Apr": 3,
    "May": 4,
    "Jun": 5,
    "Jul": 6,
    "Aug": 7,
    "Sep": 8,
    "Oct": 9,
    "Nov": 10,
    "Dec": 11
}

def date_sort(e):
    return months[e.get_due_date()[0:3]] * 100 + int(e.get_due_date().split()[1][0:-1])

def title_sort(e):
    return e.get_title()

def complete_sort(e):
    if e.get_completed():
        return "Complete"
    return "Incomplete"

def grade_sort(e):
    if e.get_max_points() == 0:
        return 0
    return float(100.0 * e.get_points() / e.get_max_points())

import datetime
from flask import Flask, render_template, url_for, request, redirect, json
from client import DatabaseWrapper
from classes import Class
from datetime import datetime

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

app = Flask(__name__)

db = DatabaseWrapper("db/apollo.db")

db.open_connection()
db.open_cursor()

db.load_semesters()
db.load_classes()
db.load_assignments()
db.load_notes()

user = db.get_user()

db.close_connection()

@app.before_request
def before_request():
    db.open_connection()
    db.open_cursor()

    if db.sort_func == 'date':
        db.assignments.sort(key=date_sort)

# Main home page
@app.route('/index')
@app.route('/home')
@app.route('/')
def index(name=None):
    active_semester = db.active_semester
    semesters = db.semesters

    return render_template('index.html',
        url_for         = url_for,
        semesters       = semesters,
        str             = str,
        active_semester = active_semester,
        user            = user
    )

@app.route('/notes/edit/<note_id>', methods=['GET', 'POST'])
def edit_note(note_id=None):
    active_semester = db.active_semester
    classes = db.classes

    note = None
    for n in db.notes:
        if n.get_uuid() == int(note_id):
            note = n
            break

    if note == None:
        redirect(url_for('notes'))

    temp = db.select_class_with_id(note.get_class_id())
    class_ = Class(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7])

    if request.method == "POST":
        if request.form.get('save') == 'save':
            print(request.form)

            date = ""
            temp_datetime = datetime.now()
            date += temp_datetime.strftime("%b") + " "
            date += str(int(temp_datetime.strftime("%d"))) + ","
            date += temp_datetime.strftime("%G") + " "
            date += temp_datetime.strftime("%X")

            title      = request.form.get('title')
            author     = request.form.get('author')
            body       = request.form.get('note_body')
            class_id   = request.form.get('class_selector')

            db.update_note(
                note.get_uuid(),
                title,
                date,
                author,
                body,
                class_id
            )
        
        return redirect(url_for('notes'))

    return render_template('edit_note.html',
        note                = note,
        active_semester     = active_semester,
        classes             = classes,
        str                 = str,
        user                = user,
        class_              = class_,
        int                 = int
    )

# See every note for each class that can be accessed via their own page
# (through routing?)
@app.route('/notes', methods=['GET', 'POST'])
def notes(name=None):
    active_semester = db.active_semester
    classes         = db.classes
    notes           = db.notes

    if request.method == "POST":
        if request.form.get('btn') == 'Add':
            date = ""
            temp_datetime = datetime.now()
            date += temp_datetime.strftime("%b") + " "
            date += str(int(temp_datetime.strftime("%d"))) + ","
            date += temp_datetime.strftime("%G") + " "
            date += temp_datetime.strftime("%X")

            title      = request.form.get('title')
            author     = request.form.get('author')
            body       = request.form.get('note_body')
            class_id   = request.form.get('class_selector')

            db.insert_note(title, date, author, body, "", class_id)

        elif request.form.get('delete') == 'delete':
            note_id = request.form.get('note_id')
            db.delete_note(note_id)

        elif type(str(request.form.get('edit'))) == str:
            return redirect(url_for('edit_note', note_id=request.form.get('edit')))

        return redirect(url_for('notes'))

    return render_template('notes.html',
        url_for         = url_for,
        classes         = classes,
        active_semester = active_semester,
        str             = str,
        notes           = notes,
        user            = user,
        int             = int,
        len             = len
    )

@app.route('/assignments/edit/<assignment_id>', methods=['GET', 'POST'])
def edit_assignment(assignment_id=None):
    active_semester = db.active_semester
    classes = db.classes

    assignment = None
    for a in db.assignments:
        if a.get_uuid() == int(assignment_id):
            assignment = a
            break

    if assignment == None:
        redirect(url_for('assignments'))

    temp = db.select_class_with_id(assignment.get_class_id())

    class_ = Class(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7])
    if request.method == "POST":
        if request.form.get('save') == 'save':
            title      = request.form.get('title')
            due_date   = request.form.get('due_date')
            completed  = request.form.get('completed')
            points     = request.form.get('points')
            max_points = request.form.get('max_points')
            weight     = request.form.get('weight')
            link       = request.form.get('link')

            db.update_assignment(
                assignment.get_uuid(),
                title,
                due_date,
                completed,
                points,
                max_points,
                weight,
                link
            )
        return redirect(url_for('assignments'))

    return render_template('edit_assignment.html',
        assignment          = assignment,
        active_semester     = active_semester,
        classes             = classes,
        str                 = str,
        class_              = class_
    )

# See every due/completed assignment for each class (with cool metrics)
@app.route('/assignments', methods=['GET', 'POST'])
def assignments(name=None):
    active_semester = db.active_semester
    classes = db.classes
    assignments = db.assignments

    if request.method == "POST":
        if request.form.get('btn') == 'Add':
            title      = request.form.get('title')
            due_date   = request.form.get('due_date')
            completed  = request.form.get('completed')
            points     = request.form.get('points').encode('ascii', 'ignore')
            max_points = request.form.get('max_points').encode('ascii', 'ignore')
            weight     = request.form.get('weight').encode('ascii', 'ignore')
            link       = request.form.get('link')
            class_id   = request.form.get('class_selector')

            if points == '':
                points = 0.0

            if max_points == '':
                max_points = 0.0

            if weight == '':
                weight = 0.0

            if title and due_date and class_id:
                db.insert_assignment(
                    title,
                    due_date,
                    completed,
                    points,
                    max_points,
                    weight,
                    link,
                    class_id
                )
        elif request.form.get('btn') == 'Sort':
            sort_function = str(request.form.get('sort_selector'))
            if sort_function == 'date':
                if db.sort_func == 'date':
                    db.sort_func = ''
                    db.assignments.sort(key=date_sort, reverse=True)
                else:
                    db.assignments.sort(key=date_sort)
                    db.sort_func = 'date'
            elif sort_function == 'title':
                if db.sort_func == 'title':
                    db.sort_func = ''
                    db.assignments.sort(key=title_sort, reverse=True)
                else:
                    db.sort_func = 'title'
                    db.assignments.sort(key=title_sort)
            elif sort_function == 'complete':
                if db.sort_func == 'complete':
                    db.sort_func = ''
                    db.assignments.sort(key=complete_sort, reverse=True)
                else:
                    db.sort_func = 'complete'
                    db.assignments.sort(key=complete_sort)
            elif sort_function == 'grade':
                if db.sort_func == 'grade':
                    db.sort_func = ''
                    db.assignments.sort(key=grade_sort, reverse=True)
                else:
                    db.sort_func = 'grade'
                    db.assignments.sort(key=grade_sort)

        elif request.form.get('delete') == 'delete':
            assignment_id = int(request.form['assignment_id'])
            db.delete_assignment(assignment_id)

        elif type(str(request.form.get('edit'))) == str:
            return redirect(url_for('edit_assignment', assignment_id=int(request.form.get('edit'))))

        return redirect('assignments')

    return render_template('assignments.html',
        url_for         = url_for,
        active_semester = active_semester,
        classes         = classes,
        assignments     = assignments,
        str             = str
    )

# Edit a class database object
@app.route('/calendar/edit/<class_id>', methods=['GET', 'POST'])
def edit_calendar(class_id=None):
    active_semester = db.active_semester
    course = None
    for c in db.classes:
        if c.get_uuid() == int(class_id):
            course = c
            break

    if course == None:
        return redirect(url_for('calendar'))

    if request.method == "POST":
        if request.form.get('cancel') == 'cancel':
            return redirect(url_for('calendar'))
        elif request.form.get('save') == 'save':
            db.update_class(
                course.get_uuid(),
                request.form.get('prefix'),
                request.form.get('course_number'),
                request.form.get('instructor'),
                request.form.get('meet_days'),
                request.form.get('start_time'),
                request.form.get('end_time')
            )
            return redirect(url_for('calendar'))

    return render_template('edit_calendar.html',
        course          = course,
        active_semester = active_semester,
        str             = str
    )

# See class enrollment and weekly schedule
@app.route('/calendar', methods=['GET', 'POST'])
def calendar(name=None):
    active_semester = db.active_semester
    classes = [c for c in db.classes if int(c.get_semester_id()) == int(active_semester.get_uuid())]

    if request.method == "POST":
        if request.form.get('btn') == 'Add':
            prefix        = request.form.get('prefix')
            course_number = request.form.get('course_number')
            instructor    = request.form.get('instructor')
            meet_days     = request.form.get('meet_days')
            start_time    = request.form.get('start_time')
            end_time      = request.form.get('end_time')
            semester_id   = active_semester.get_uuid()

            if prefix != "" or course_number != "" or instructor != "" or meet_days != "" \
            or start_time != "" or end_time != "" or semester_id != "":
                db.insert_class(
                    prefix,
                    course_number,
                    instructor,
                    meet_days,
                    start_time,
                    end_time,
                    semester_id
                )

        elif request.form.get('delete') == 'delete':
            class_id = request.form['class_']
            db.delete_class(class_id)

        elif request.form.get('edit') == 'edit':
            return redirect(url_for('edit_calendar',
                class_id = int( request.form['class_'])
            ))
            
        return redirect(url_for('calendar'))

    return render_template('calendar.html',
        url_for         = url_for,
        active_semester = active_semester,
        classes         = classes,
        len             = len,
        str             = str,
        int             = int,
        json            = json
    )

# Access and add/update semesters
@app.route('/settings', methods=['GET', 'POST'])
def settings(name=None):
    active_semester = db.active_semester
    semesters = db.semesters
    db.save_changes()

    if request.method == "POST":
        if request.form['btn'] == 'Add':
            select_season = request.form.get('semester_season')
            select_year   = request.form.get('semester_year')

            db.insert_semester(select_season, select_year)
        elif request.form['btn'] == 'Select':
            db.activate_a_semester(int(request.form.get('active_semester')))

        return redirect(url_for('settings'))

    return render_template('settings.html',
        url_for         = url_for,
        semesters       = semesters,
        str             = str,
        active_semester = active_semester
    )

@app.after_request
def after_request(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['Cache-Control'] = 'no-cache, no-store'
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['pragma'] = 'no-cache'

    if db.is_open:
        db.save_changes()
        db.close_connection()

    return response
