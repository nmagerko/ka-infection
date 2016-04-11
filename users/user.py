from users.classroom import UserClassroom
from users.relationship import UserRelationship

DEFAULT_MAJOR_VERSION = 1
DEFAULT_MINOR_VERSION = 0

class User(object):

	# a static identifier is used to make classrooms easier to identify
	# and to allow for the construction of obvious hash values
	__ID = 0

	def __init__(self):
		"""
		Initializes a new User
		"""

		self._id = User.__ID
		self._colleagues = []
		self._relationships = {}

		self.version = (DEFAULT_MAJOR_VERSION, DEFAULT_MINOR_VERSION)
		self.classroom = UserClassroom(self)

		User.__ID += 1

	@property
	def id(self):
		return self._id

	def set_version(self, version):
		"""
		Recursively sets the version of this user and all users related to it
		args:
			version: a tuple containing the major and minor version
		"""

		if self.version == version:
			return

		self.version = version

		for colleague in self._colleagues:
			colleague.set_version(version)

	def set_version_limited(self, version, limit):
		"""
		Exactly like set_version, but only sets a maximum number of users'
		versions at a time
		args:
			version: a tuple containing the major and minor version
			limit: the maximum number of users to update
		returns:
			The number of users updated
		"""

		if self.version == version or limit <= 0:
			return 0


		self.version = version
		updated = 1

		for colleague in self._colleagues:
			updated += colleague.set_version_limited(version, limit - updated)

		return updated

	def set_classroom(self, classroom):
		"""
		Recursively sets the classroom of this user and all users related to it
		args:
			classroom: a UserClassroom instance
		"""

		if self.classroom == classroom:
			return

		self.classroom = classroom

		for colleague in self._colleagues:
			colleague.set_classroom(classroom)

	def add_relationship(self, user, relationship):
		"""
		Adds a relationship between this user and the given user, merging
		their classrooms as necessary
		args:
			user: a User instance
			relationship: a UserRelationship value
		"""

		self._colleagues.append(user)
		self._relationships[user] = relationship

		user._colleagues.append(self)
		user._relationships[self] = UserRelationship.invert(relationship)

		prevClassroom = user.classroom
		self.classroom.update(user)

	### built-in overrides ###

	def __hash__(self):
		return self._id

	def __eq__(self, other):
		return self._id == other._id if other is not None else False

	def __ne__(self, other):
		return not self.__eq__(other)

	def __str__(self):
		relationships = []
		for k in self._colleagues:
			relationships.append({ k.id: UserRelationship.stringify( \
				self._relationships[k]) })

		return "{{ ID: {0}, Version: {1}, Class: {2}, Relationships: {3} }}" \
			.format(self.id, self.version, self.classroom, relationships)

	def __repr__(self):
		return self.__str__()
