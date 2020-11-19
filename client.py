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

import sqlite3
import uuid
from semester   import Semester
from user       import User
from classes    import Class
from assignment import Assignment
from note       import Note

class DatabaseWrapper:
    def __init__(self, filename):
        self.filename = filename
        self.is_open  = False

        self.active_semester = Semester(0, "", 0, 0, 0)

        self.semesters   = []
        self.notes       = []
        self.assignments = []
        self.classes     = []

        self.sort_func = "date"
        #self.users = []

    """
    General purpose database operations
    """

    # open connection to database
    def open_connection(self):
        print("Opening database connection to %s" % self.filename)
        self.conn    = sqlite3.connect(self.filename, check_same_thread=False)
        self.is_open = True

    # close connection to database
    def close_connection(self):
        print("Closing database connection to %s" % self.filename)
        self.conn.close()
        self.is_open = False

    # get sqlite3 cursor so we can input queries
    def open_cursor(self):
        self.c = self.conn.cursor()

    # execute SQL queries made with the active cursor
    def save_changes(self):
        self.conn.commit()


    """
    Semester operations
    """

    # load database objects into program memory
    def load_semesters(self):
        semesters = self.select_semesters()
        self.save_changes()
        for s in semesters:
            temp = Semester(
                s[0], # uuid
                s[1], # season
                s[2], # year
                s[3], # is active
                s[4]  # num classes
            )

            if temp.get_active():
                self.active_semester = temp

            self.semesters.append(temp)


    # insert new semester
    def insert_semester(self, season, year):
        if season == None or year == None or season == "Choose the season" or year == "Choose the year":
            print('Attempted to insert an invalid semester object.')
            return

        temp = Semester(self.get_uuid(), season, year, 0, 0)
        self.semesters.append(temp)
        self.c.execute("""INSERT INTO SEMESTER(SEMESTER_ID,
                                               SEMESTER_SEASON,
                                               SEMESTER_YEAR,
                                               SEMESTER_ACTIVE,
                                               SEMESTER_NUM_CLASSES)
                               VALUES (?, ?, ?, ?, ?)""", (
                                    temp.get_uuid(),
                                    temp.get_season(),
                                    temp.get_year(),
                                    temp.get_active(),
                                    temp.get_num_classes()
                                )
                        )

        self.save_changes()

    # fetch semesters
    def select_semesters(self):
        self.c.execute('SELECT * FROM SEMESTER')
        return self.c.fetchall()

    # activate a single semester
    def activate_a_semester(self, semester_id):
        for s in self.semesters:
            if s.get_uuid() == int(semester_id):
                s.set_active(True)
                self.c.execute('UPDATE SEMESTER SET SEMESTER_ACTIVE=1 WHERE SEMESTER_ID=(?)',
                    (semester_id,)
                )
                self.active_semester = s
            else:
                s.set_active(False)
                self.c.execute('UPDATE SEMESTER SET SEMESTER_ACTIVE=0 WHERE SEMESTER_ID<>(?)',
                    (semester_id,)
                )

        self.save_changes()

    """
    Class operations
    """
    # get number of classes schedule today

    def load_classes(self):
        classes = self.select_class()
        self.save_changes()
        for c in classes:
            self.classes.append(Class(
                c[0], # uuid
                c[1], # prefix
                c[2], # course number
                c[3], # instructor
                c[4], # meet days
                c[5], # start time
                c[6], # end time
                c[7]  # semester id
            ))

    def select_class(self):
        self.c.execute('SELECT * FROM CLASS')
        return self.c.fetchall()

    def select_class_with_id(self, class_id):
        self.c.execute('SELECT * FROM CLASS WHERE CLASS_ID=?', (class_id,))
        return self.c.fetchone()

    def select_class_from_semester(self, semester_id):
        self.c.execute('SELECT * FROM CLASS WHERE SEMESTER_ID=?', (semester_id,))
        return self.c.fetchall()

    def insert_class(self, prefix, course_number, instructor, meet_days, start_time, end_time, semester_id):
        if not prefix or not course_number or not instructor or not meet_days or \
        not start_time or not end_time or not semester_id:
            print('Attempted to insert an invalid class object.')
            return

        temp = Class(
            self.get_uuid(),
            prefix,
            course_number,
            instructor,
            meet_days,
            start_time,
            end_time,
            semester_id
        )
        self.classes.append(temp)

        self.c.execute("""INSERT INTO CLASS(CLASS_ID,
                                            CLASS_PREFIX,
                                            CLASS_COURSE_NUMBER,
                                            CLASS_INSTRUCTOR,
                                            CLASS_MEET_DAYS,
                                            CLASS_START_TIME,
                                            CLASS_END_TIME,
                                            SEMESTER_ID)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (
                                    temp.get_uuid(),
                                    temp.get_prefix(),
                                    temp.get_course_number(),
                                    temp.get_instructor(),
                                    temp.get_meet_days(),
                                    temp.get_start_time(),
                                    temp.get_end_time(),
                                    temp.get_semester_id() 
                        ))

        # update the active semester object (increment the num classes)
        temp_semester = None
        for s in self.semesters:
            if s.uid == semester_id:
                s.set_num_classes(s.get_num_classes() + 1)
                temp_semester = s
                break

        if temp_semester:
            self.c.execute('UPDATE SEMESTER SET SEMESTER_NUM_CLASSES=? WHERE SEMESTER_ID=?',
                (temp_semester.get_num_classes(), temp.get_semester_id(),)
            )
            self.save_changes()


    def delete_class(self, class_id):
        self.c.execute('SELECT * FROM CLASS WHERE CLASS_ID=?',
            (int(class_id),)
        )
        class_ = self.c.fetchone()
        semester_id = class_[7]

        self.c.execute('DELETE FROM CLASS WHERE CLASS_ID=?',
            (int(class_id),)
        )
        self.save_changes()

        self.classes = []
        self.load_classes()

        # update the active semester object (decrement the num classes)
        temp_semester = None
        for s in self.semesters:
            if s.uid == semester_id:
                s.set_num_classes(s.get_num_classes() - 1)
                temp_semester = s
                break

        if temp_semester:
            self.c.execute('UPDATE SEMESTER SET SEMESTER_NUM_CLASSES=? WHERE SEMESTER_ID=?',
                (temp_semester.get_num_classes(), int(semester_id))
            )
            self.save_changes()

    def update_class(self, class_id, prefix, course_number, instructor, meet_days, start_time, end_time):
        self.c.execute("""UPDATE CLASS SET
            CLASS_PREFIX=?,
            CLASS_COURSE_NUMBER=?,
            CLASS_INSTRUCTOR=?,
            CLASS_MEET_DAYS=?,
            CLASS_START_TIME=?,
            CLASS_END_TIME=? WHERE CLASS_ID=?""",
            (
                str(prefix),
                int(course_number),
                str(instructor),
                str(meet_days),
                start_time,
                end_time,
                int(class_id)
            )
        )
        self.save_changes()

        self.classes = []
        self.load_classes()

    def get_n_classes_today(self, semester_id):
        return

    """
    Assignment operations
    """
    # get number of assignments completed

    def load_assignments(self):
        assignments = self.select_assignment()
        self.save_changes()
        for a in assignments:
            self.assignments.append(Assignment(
                a[0], # uuid
                a[1], # title
                a[2], # due date
                a[3], # completed
                a[4], # points
                a[5], # max points
                a[6], # weight
                a[7], # link
                a[8]  # class id
            ))

    def insert_assignment(self, title, due_date, completed, points, max_points, weight, link, class_id):
        temp = Assignment(
            self.get_uuid(),
            title,
            due_date,
            completed,
            points,
            max_points,
            weight,
            link,
            class_id
        )
        self.assignments.append(temp)

        self.c.execute("""INSERT INTO ASSIGNMENT(
                                            ASSIGNMENT_ID,
                                            ASSIGNMENT_TITLE,
                                            ASSIGNMENT_DUE_DATE,
                                            ASSIGNMENT_COMPLETED,
                                            ASSIGNMENT_POINTS,
                                            ASSIGNMENT_MAX_POINTS,
                                            ASSIGNMENT_WEIGHT,
                                            ASSIGNMENT_LINK,
                                            CLASS_ID)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                                    temp.get_uuid(),
                                    temp.get_title(),
                                    temp.get_due_date(),
                                    temp.get_completed(),
                                    temp.get_points(),
                                    temp.get_max_points(),
                                    temp.get_weight(),
                                    temp.get_link(),
                                    temp.get_class_id() 
                        ))
        self.save_changes()

    def delete_assignment(self, assignment_id):
        self.c.execute('DELETE FROM ASSIGNMENT WHERE ASSIGNMENT_ID=?',
            (int(assignment_id),)
        )
        self.save_changes()

        self.assignments = []
        self.load_assignments()

    def update_assignment(self, assignment_id, title, due_date, completed, points=0, max_points=0, weight=0, link=""):
        self.c.execute("""UPDATE ASSIGNMENT SET
                    ASSIGNMENT_TITLE=?,
                    ASSIGNMENT_DUE_DATE=?,
                    ASSIGNMENT_COMPLETED=?,
                    ASSIGNMENT_POINTS=?,
                    ASSIGNMENT_MAX_POINTS=?,
                    ASSIGNMENT_WEIGHT=?,
                    ASSIGNMENT_LINK=? WHERE ASSIGNMENT_ID=?""", (
                        str(title),
                        str(due_date),
                        int(str(completed).lower() == 'true'),
                        float(points),
                        float(max_points),
                        float(weight),
                        str(link),
                        int(assignment_id)
                    )
        )
        self.save_changes()

        self.assignments = []
        self.load_assignments()

    def select_assignment(self):
        self.c.execute('SELECT * FROM ASSIGNMENT')
        return self.c.fetchall()

    def get_n_assignments_completed(self, class_id):
        return

    def get_n_assignments(self, class_id):
        self.c.execute('SELECT * FROM ASSIGNMENT WHERE CLASS_ID=?', (int(class_id),))
        return len(self.c.fetchall())

    def get_n_assignments_style_height(self, class_id):
        self.c.execute('SELECT * FROM ASSIGNMENT WHERE CLASS_ID=?', (int(class_id),))
        return len(self.c.fetchall()) * 55

    """
    Note operations
    """

    def load_notes(self):
        notes = self.select_note()
        self.save_changes()
        for a in notes:
            self.notes.append(Note(
                a[0], # uuid
                a[1], # title
                a[2], # date
                a[3], # author
                a[4], # body
                a[5], # flairs
                a[6] # class_id
            ))

    def insert_note(self, title, date, author, body, flairs, class_id):
        temp = Note(
            self.get_uuid(),
            title,
            date,
            author,
            body,
            flairs,
            class_id
        )
        self.notes.append(temp)

        self.c.execute("""INSERT INTO NOTE(
                                        NOTE_ID,
                                        NOTE_TITLE,
                                        NOTE_DATE,
                                        NOTE_AUTHOR,
                                        NOTE_BODY,
                                        NOTE_FLAIRS,
                                        CLASS_ID)
                               VALUES (?, ?, ?, ?, ?, ?, ?)""", (
                                    temp.get_uuid(),
                                    temp.get_title(),
                                    temp.get_date(),
                                    temp.get_author(),
                                    temp.get_body(),
                                    temp.get_flairs(),
                                    temp.get_class_id()
                        ))
        self.save_changes()

    def delete_note(self, note_id):
        self.c.execute("""DELETE FROM NOTE WHERE NOTE_ID=?""", (note_id,))
        self.save_changes()

        self.notes = []
        self.load_notes()

    def update_note(self, note_id, title, date, author, body, class_id):
        self.c.execute("""UPDATE NOTE SET
                                        NOTE_TITLE=?,
                                        NOTE_DATE=?,
                                        NOTE_AUTHOR=?,
                                        NOTE_BODY=?,
                                        CLASS_ID=?
                                WHERE NOTE_ID=?""", (
                                    str(title),
                                    str(date),
                                    str(author),
                                    str(body),
                                    int(class_id),
                                    int(note_id)
                        ))
        self.save_changes()

        self.notes = []
        self.load_notes()

    def select_note(self):
        self.c.execute("SELECT * FROM NOTE");
        return self.c.fetchall()

    def select_note_with_id(self, note_id):
        self.c.execute("SELECT * FROM NOTE WHERE NOTE_ID=?", (note_id,))
        return self.c.fetchone()

    # get number of notes with equal class id
    def get_n_notes(self, class_id):
        self.c.execute("SELECT * FROM NOTE WHERE CLASS_ID=?", (class_id,))
        return len(self.c.fetchall())

    """
    Misc
    """

    # fetch my user object
    def get_user(self):
        self.c.execute('SELECT * FROM USER WHERE USER_ID=1')
        user_db = self.c.fetchone()
        return User(user_db[0], user_db[1], user_db[2])

    # output all objects in the assignments table
    def print_assignments(self):
        self.c.execute('SELECT * FROM ASSIGNMENT')

    # output all objects in the notes table
    def notes_assignments(self):
        self.c.execute('SELECT * FROM NOTE')

    # get a unique 32-bit integer ID
    def get_uuid(self):
        return uuid.uuid4().int >> 96