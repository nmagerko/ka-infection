class UserRelationship(object):

	# enumerations of the possible relationships between two Users
	# "BOTH" implies two Users teach each other
	STUDENT = 0
	TEACHER = 1
	BOTH = 2

	@classmethod
	def invert(cls, relationship):
		"""
		Gives the opposite of the provided UserRelationship
		args:
			relationship: an integer-valued UserRelationship
		returns:
			A UserRelationship value
		"""

		if relationship == cls.STUDENT:
			return cls.TEACHER
		if relationship == cls.TEACHER:
			return cls.STUDENT
		return cls.BOTH

	@classmethod
	def stringify(cls, relationship):
		"""
		Converts the provided UserRelationship into its string form
		args:
			relationship: an integer-valued UserRelationship
		returns:
			A UserRelationship in string form
		"""

		if relationship == cls.STUDENT:
			return "STUDENT"
		if relationship == cls.TEACHER:
			return "TEACHER"
		if relationship == cls.BOTH:
			return "BOTH"
		return "ERROR"
