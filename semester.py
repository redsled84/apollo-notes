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

class Semester:
	# constructor
	def __init__(self, uid, season, year, active, num_classes):
		self.set_uuid(uid)
		self.set_season(season)
		self.set_year(year)
		self.set_active(active)
		self.set_num_classes(num_classes)

	# object to string
	def __str__(self):
		return ""
		# return "<Semester> ID: " + str(self.uid) + \
		#       " Season: %8s" % (self.season,) + \
		#       " Year: " + str(self.year) + \
		#       " Active: " + str(bool(self.active)) \
		#       " Num Classes: " + str(self.num_classes)

	# getters
	def get_uuid(self):
		return int(self.uid)

	def get_season(self):
		return self.season

	def get_year(self):
		return self.year

	def get_active(self):
		return self.active

	def get_num_classes(self):
		return self.num_classes

	def get_title(self):
		return str(self.get_season()) + " " + str(self.get_year())

	# setters
	def set_uuid(self, uid):
		self.uid          = int(uid)

	def set_season(self, s):
		self.season       = str(s)

	def set_year(self, yr):
		self.year         = int(yr)

	def set_active(self, active):
		self.active       = bool(active)

	def set_num_classes(self, num_classes):
		self.num_classes  = int(num_classes)


