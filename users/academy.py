class UserAcademy(object):

	def __init__(self, users):
		"""
		Initializes a new UserAcademy
		args:
			users: a list of users to add to the academy.
		NOTE that although Users are mutable, they should not be modified after
		being added to the academy; modification may result in skewed infections
		"""

		self._classrooms = []
		self._extrapolate_classrooms(users)

	def _extrapolate_classrooms(self, users):
		"""
		Extrapolates the classrooms from the list of users, ensuring
		that no classrooms are repeated
		args:
			users: a list of User instances
		"""

		table = {}
		for user in users:
			classroom = user.classroom

			if not classroom in table:
				table[classroom] = True
				self._classrooms.append(classroom)

		# the classrooms are sorted to facilitate the procedure used by
		# the basic limited infection algorithm
		self._classrooms = sorted(self._classrooms, key=lambda c: c.size)

	@classmethod
	def total_infection(cls, version, user):
		"""
		Infects all users including and related to the given user
		with the provided version. As this is not dependent on the
		Academy itself, it is a class method
		args:
			version: a tuple representing the version with which to infect
			user: a User instance
		"""

		if user is not None:
			user.set_version(version)

	def limited_infection(self, version, target):
		"""
		Infects students up to a target number by proceeding sequentially
		(from smallest to largest) through the maximally related subsets of
		users in the academy. Subsets will be infected even if not all of the
		users contained in it can be infected
		args:
			version: a tuple representing the version with which to infect
			target: the maximum number of users to infect
		returns:
			The number of users that were infected
		"""

		infected = 0

		for classroom in self._classrooms:
			result = infected + classroom.size

			if result <= target:
				classroom.contact.set_version(version)
				infected = result
			else:
				difference = target - infected
				classroom.contact.set_version_limited(version, difference)

		return infected

	def limited_infection_enhanced(self, version, target):
		"""
		Attempts to infect exactly the target number of students in the
		academy, but does nothing unless some combination of maximally related
		subsets of students can be completely infected
		args:
			version: a tuple representing the version with which to infect
			target: the number of users to infect
		"""

		infect = self._limited_infection_enhanced(target)
		for index in infect:
			self._classrooms[index].contact.set_version(version)

	def _limited_infection_enhanced(self, target):
		"""
		Helper method for limited_infection_enhanced.
		Implements the dynamic programming solution for the subset sum problem
		(https://en.wikipedia.org/wiki/Subset_sum_problem) to determine which
		classrooms can be infected to reach the target sum
		args:
			target: the number of users to infect
		returns:
			A list of indicies corresponding to the classrooms that should be
			infected
		"""

		size = len(self._classrooms)
		valid = [[x for x in range(0, target + 1)] for x in range(0, size + 1)]

		# set up the first column to be True, since all empty subsets
		# sum to zero; set up the first row to be False, since empty
		# subsets cannot sum to zero
		for i in range(0, size + 1):
			valid[i][0] = True
		for j in range(1, target + 1):
			valid[0][j] = False

		# note that the work above allows us to exclude extra bounds checks
		for i in range(1, size + 1):
			for j in range(1, target + 1):
				prev_valid = valid[i - 1][j]
				value = self._classrooms[i - 1].size

				if value > j:
					# we cannot form the sum with the current value, so we
					# use the truth value of the subset from the previous iteration
					valid[i][j] = prev_valid
				else:
					# otherwise, we can either form the sum using a previous
					# subset alone, or using  a combination of this value and
					# a subset from a previous iteration
					valid[i][j] = prev_valid or valid[i - 1][j - value]

		indicies = []

		# we were not able to find the exact sum
		if not valid[size][target]:
			return indicies

		# backtrack to find exactly which elements contributed to sum
		i, j = size, target
		while i > 0:
			result = valid[i][j]
			result_above = valid[i - 1][j]

			# we really only care when the truth value of the element
			# above the current one changed, since that means the current
			# element was in combination with some previous subset
			if result and not result_above:
				indicies.append(i - 1)
				j -= self._classrooms[i - 1].size

			i -= 1

		return indicies
