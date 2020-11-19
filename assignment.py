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

class Assignment:
    # constructor
    def __init__(self, uid, title, due_date, completed=False, points=0.0, max_points=0.0, weight=0.0, link="", class_id=None):
        self.set_uuid(uid)
        self.set_title(title)
        self.set_due_date(due_date)
        self.set_completed(completed)
        self.set_points(points)
        self.set_max_points(max_points)
        self.set_weight(weight)
        self.set_link(link)
        self.set_class_id(class_id)

    def __str__(self):
        return self.title + " " + self.due_date

    def to_json(self):  # New special method
        grade = 0
        if self.get_max_points() > 0:
            grade = self.get_points() / self.get_max_points()
        return [ self.get_class_id(), self.get_due_date(), grade, self.get_weight()]

    # getters
    def get_uuid(self):
        return int(self.uid)

    def get_title(self):
        return self.title

    def get_due_date(self):
        return self.due_date

    def get_completed(self):
        return self.completed

    def get_link(self):
        if self.link is None:
            return ""
        return self.link

    def get_points(self):
        return float(self.points)

    def get_max_points(self):
        return float(self.max_points)

    def get_weight(self):
        if self.weight is None:
            return 0.0
        return self.weight

    def get_class_id(self):
        return int(self.class_id)

    # setters
    def set_uuid(self, uid):
        self.uid       = int(uid)

    def set_title(self, title):
        self.title     = str(title)

    def set_due_date(self, due_date):
        self.due_date  = str(due_date)

    def set_completed(self, completed):
        self.completed = bool(completed)

    def set_link(self, link):
        self.link      = str(link)

    def set_points(self, points):
        self.points = points

    def set_max_points(self, max_points):
        self.max_points = max_points

    def set_weight(self, weight):
        self.weight = float(weight)

    def set_class_id(self, class_id):
        self.class_id  = int(class_id)
