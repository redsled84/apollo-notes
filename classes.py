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

class Class:
    # constructor
    def __init__(self, uid, prefix, course_number, instructor, meet_days, start_time, end_time, semester_id):
        self.set_uuid(uid)
        self.set_prefix(prefix)
        self.set_course_number(course_number)
        self.set_instructor(instructor)
        self.set_meet_days(meet_days)
        self.set_start_time(start_time)
        self.set_end_time(end_time)
        self.set_semester_id(semester_id)

    def to_json(self):  # New special method.
        """ Convert to JSON format string representation. """
        return [ self.get_title(), self.get_meet_days(), self.get_start_time(), self.get_end_time(), self.get_uuid() ]

    # getters
    def get_uuid(self):
        return int(self.uid)

    def get_prefix(self):
        return self.prefix

    def get_course_number(self):
        return self.course_number

    def get_instructor(self):
        return self.instructor

    def get_meet_days(self):
        return self.meet_days

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def get_semester_id(self):
        return int(self.semester_id)

    def get_title(self):
        return str(self.get_prefix()) + " " + str(self.get_course_number())

    # setters
    def set_uuid(self, uid):
        self.uid           = int(uid)

    def set_prefix(self, prefix):
        self.prefix        = str(prefix)

    def set_course_number(self, course_number):
        self.course_number = int(course_number) 

    def set_instructor(self, instructor):
        self.instructor    = str(instructor)

    def set_meet_days(self, meet_days):
        self.meet_days     = str(meet_days)

    def set_start_time(self, start_time):
        self.start_time     = str(start_time)

    def set_end_time(self, end_time):
        self.end_time     = str(end_time)

    def set_semester_id(self, semester_id):
        self.semester_id   = str(semester_id)