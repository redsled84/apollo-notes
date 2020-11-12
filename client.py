import sqlite3
import uuid
from semester import Semester
from user import User
from classes import Class

class DatabaseWrapper:
    def __init__(self, filename):
        self.filename = filename
        self.is_open  = False

        self.active_semester = Semester(0, "", 0, 0, 0)

        self.semesters   = []
        self.notes       = []
        self.assignments = []
        self.classes     = []
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

    def select_class_from_semester(self, semester_id):
        self.c.execute('SELECT * FROM CLASS WHERE SEMESTER_ID=?', (semester_id,))
        return self.c.fetchall()

    def insert_class(self, prefix, course_number, instructor, meet_days, start_time, end_time, semester_id):
        if prefix == "" or course_number == "" or instructor == "" or meet_days == "" or \
        start_time == "" or end_time == "" or semester_id == "":
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

        if temp.semester_id in self.semesters:
            print 'true'

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
                (temp_semester.get_num_classes(), int(class_[7]))
            )
            self.save_changes()

    def update_class(self, class_id, prefix, course_number, instructor, meet_days, start_time, end_time):
        self.c.execute('SELECT * FROM CLASS WHERE CLASS_ID=?',
            (int(class_id),)
        )
        class_ = self.c.fetchone()
        self.save_changes()

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
        return

    def insert_assignment(self):
        return

    def delete_assignment(self):
        return

    def update_assignment(self):
        return

    def get_n_assignments_completed(self, class_id):
        return

    def get_n_assignments(self, class_id):
        return

    """
    Note operations
    """

    def load_notes(self):
        return

    def insert_note(self):
        return

    def delete_note(self):
        return

    def update_note(self):
        return

    def get_n_notes(self, class_id):
        return

    # get number of notes

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