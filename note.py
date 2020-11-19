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

class Note:
	# constructor
	def __init__(self, uid, title, date, author, body, flairs, class_id):
		self.set_uuid(uid)
		self.set_title(title)
		self.set_date(date)
		self.set_author(author)
		self.set_body(body)
		self.set_flairs(flairs)
		self.set_class_id(class_id)

	# getters
	def get_uuid(self):
		return self.uid

	def get_title(self):
		return self.title

	def get_date(self):
		return self.date

	def get_author(self):
		return self.author

	def get_body(self):
		return self.body

	def get_flairs(self):
		return self.flairs

	def get_class_id(self):
		return self.class_id

	# setters
	def set_uuid(self, uid):
		self.uid = uid

	def set_title(self, title):
		self.title = title

	def set_date(self, date):
		self.date = date

	def set_author(self, author):
		self.author = author

	def set_body(self, body):
		self.body = body

	def set_flairs(self, flairs):
		self.flairs = flairs

	def set_class_id(self, class_id):
		self.class_id = class_id