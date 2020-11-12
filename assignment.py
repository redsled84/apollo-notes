class Assignment:
	# constructor
	def __init__(self, uid, title, due_date, link, completed, class_id):
		self.set_uuid(uid)
		self.set_title(title)
		self.set_due_date(due_date)
		self.set_link(link)
		self.set_completed(completed)
		self.set_class_id(class_id)

	# getters
	def get_uuid(self):
		return self.uid

	def get_title(self):
		return self.title

	def get_due_date(self):
		return self.due_date

	def get_link(self):
		return self.link

	def get_completed(self):
		return self.completed

	def get_class_id(self):
		return self.class_id

	# setters
	def set_uuid(self, uid):
		self.uid       = int(uid)

	def set_title(self, title):
		self.title     = str(title)

	def set_due_date(self, due_date):
		self.due_date  = str(due_date)

	def set_link(self, link):
		self.link      = str(link)

	def set_completed(self, completed):
		self.completed = bool(completed)

	def set_class_id(self, class_id):
		self.class_id  = str(class_id)