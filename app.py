from flask import Flask, render_template, url_for, request, redirect
from client import DatabaseWrapper

app = Flask(__name__)

db = DatabaseWrapper("db/apollo.db")

db.open_connection()
db.open_cursor()

db.load_semesters()
db.load_classes()

user = db.get_user()

db.close_connection()

@app.before_request
def before_request():
    db.open_connection()
    db.open_cursor()

# Main home page
@app.route('/index')
@app.route('/home')
@app.route('/')
def index(name=None):
    active_semester = db.active_semester
    semesters = db.semesters
    db.save_changes()

    return render_template('index.html', url_for=url_for, semesters=semesters, str=str, active_semester=active_semester, user=user)

# See every note for each class that can be accessed via their own page
# (through routing?)
@app.route('/notes')
def notes(name=None):
    active_semester = db.active_semester

    return render_template('notes.html', url_for=url_for, active_semester=active_semester, str=str)

# See every due/completed assignment for each class (with cool metrics)
@app.route('/assignments')
def assignments(name=None):
    active_semester = db.active_semester

    return render_template('assignments.html', url_for=url_for, active_semester=active_semester, str=str)

# See class enrollment and weekly schedule
@app.route('/calendar', methods=['GET', 'POST'])
def calendar(name=None):
    active_semester = db.active_semester
    classes = db.classes

    if request.method == "POST":
        if request.form['btn'] == 'Add':
            prefix        = request.form.get('prefix')
            course_number = request.form.get('course_number')
            instructor    = request.form.get('instructor')
            meet_days     = request.form.get('meet_days')
            start_time    = request.form.get('start_time')
            end_time      = request.form.get('end_time')
            semester_id   = active_semester.get_uuid()

            if prefix != "" or course_number != "" or instructor != "" or meet_days != "" \
            or start_time != "" or end_time != "" or semester_id != "":
                db.insert_class(prefix, course_number, instructor, meet_days, start_time, end_time, semester_id)
                db.save_changes()

        return redirect(url_for('calendar'))


    return render_template('calendar.html', url_for=url_for, active_semester=active_semester, classes=classes, len=len, str=str, int=int)

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
            db.save_changes()
        elif request.form['btn'] == 'Select':
            db.activate_a_semester(int(request.form.get('active_semester')))

        return redirect(url_for('settings'))

    return render_template('settings.html', url_for=url_for, semesters=semesters, str=str, active_semester=active_semester)

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
