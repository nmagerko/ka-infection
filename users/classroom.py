class UserClassroom(object):

	# a static identifier is used to make classrooms easier to identify
	# and to allow for the construction of obvious hash values
	__ID = 0

	def __init__(self, contact):
		"""
		Initializes a new UserClassroom
		args:
			contract: a User to act as a contact for the entire class
		"""

		self._id = UserClassroom.__ID
		self._contact = contact
		self.size = 1

		UserClassroom.__ID += 1

	@property
	def id(self):
		return self._id

	@property
	def contact(self):
		return self._contact

	def update(self, user):
		"""
		Merges the contents of two classrooms if the given user's
		classroom differs from this one. Necessary when a student
		with relationships in multiple existing classrooms is added
		args:
			user: the User from (potentially) another classroom
		"""

		if self == user.classroom:
			return

		self.size += user.classroom.size
		user.set_classroom(self)

	### built-in overrides ###

	def __hash__(self):
		return self._id

	def __eq__(self, other):
		return self._id == other._id if other is not None else False

	def __ne__(self, other):
		return not self.__eq__(other)

	def __str__(self):
		return "{{ ID: {0}, Size: {1} }}".format(self.id, self.size)

	def __repr__(self):
		return self.__str__()
