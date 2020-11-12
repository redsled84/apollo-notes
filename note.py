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