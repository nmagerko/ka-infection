from users import *

def _setup_limited_infection():
	"""
	Sets up a list of users for the limited infection test
	(one component of 4 students, one component of 1 student)
	"""

	users = [User() for x in range(0, 5)]
	users[0].add_relationship(users[1], UserRelationship.STUDENT)
	users[1].add_relationship(users[2], UserRelationship.STUDENT)
	users[0].add_relationship(users[3], UserRelationship.STUDENT)

	return users

def _setup_enhanced_infection():
	"""
	Sets up a list of users for the enhanced infection test
	(two components of 3 students, two of 2 students)
	"""

	users = [User() for x in range(0, 10)]
	users[0].add_relationship(users[1], UserRelationship.STUDENT)
	users[0].add_relationship(users[2], UserRelationship.STUDENT)
	users[3].add_relationship(users[4], UserRelationship.STUDENT)
	users[5].add_relationship(users[6], UserRelationship.TEACHER)
	users[7].add_relationship(users[8], UserRelationship.BOTH)
	users[8].add_relationship(users[9], UserRelationship.STUDENT)

	return users

def test_infection_singular():
	"""
	Tests that the infection of a single user with
	no connections is infected correctly
	"""

	users = [User() for x in range(0, 1)]

	print "test_infection_singular: ",
	users[0].set_version((1, 1))

	try:
		assert users[0].version == (1, 1)
		print "SUCCESS"
	except AssertionError:
		print "FAIL"

def test_infection_direct():
	"""
	Tests that the infection of a single user with one or more
	other direct connections can be infected properly in either
	direction (student -> coach or coach -> student)
	"""

	users = [User() for x in range(0, 3)]
	users[0].add_relationship(users[1], UserRelationship.STUDENT)
	users[0].add_relationship(users[2], UserRelationship.STUDENT)

	# tests the coach -> student infection
	print "test_infection_direct (1/2): ",
	users[0].set_version((1, 1))
	try:
		for user in users:
			assert user.version == (1, 1)
		print "SUCCESS"
	except AssertionError:
		print "FAIL"

	# tests the student -> coach infection
	print "test_infection_direct (2/2): ",
	users[1].set_version((1, 2))
	try:
		for user in users:
			assert user.version == (1, 2)
		print "SUCCESS"
	except AssertionError:
		print "FAIL"

def test_infection_indirect():
	"""
	Tests that all users that are at least indirectly
	connected are infected properly
	"""

	users = [User() for x in range(0, 5)]
	users[0].add_relationship(users[1], UserRelationship.STUDENT)
	users[0].add_relationship(users[2], UserRelationship.STUDENT)
	users[1].add_relationship(users[3], UserRelationship.STUDENT)
	users[2].add_relationship(users[4], UserRelationship.STUDENT)

	print "test_infection_indirect: ",
	users[0].set_version((1, 1))
	try:
		for user in users:
			assert user.version == (1, 1)
		print "SUCCESS"
	except AssertionError:
		print "FAIL"

def test_infection_circular():
	"""
	Tests that all users that are connected at least indirectly
	by a cycle are infected correctly
	"""

	users = [User() for x in range(0, 4)]
	users[0].add_relationship(users[1], UserRelationship.STUDENT)
	users[1].add_relationship(users[2], UserRelationship.BOTH)
	users[2].add_relationship(users[3], UserRelationship.BOTH)
	users[3].add_relationship(users[1], UserRelationship.BOTH)

	print "test_infection_circular: ",
	users[0].set_version((1, 1))
	try:
		for user in users:
			assert user.version == (1, 1)
		print "SUCCESS"
	except AssertionError:
		print "FAIL"

def test_infection_limit():
	"""
	Tests that users infected in a limited manner
	are infected properly, and that the number of users
	infected is correct
	"""

	users = [User() for x in range(0, 5)]
	users[0].add_relationship(users[1], UserRelationship.STUDENT)
	users[1].add_relationship(users[2], UserRelationship.STUDENT)
	users[2].add_relationship(users[3], UserRelationship.STUDENT)
	users[0].add_relationship(users[4], UserRelationship.STUDENT)

	print "test_infection_limit: ",
	users[0].set_version_limited((1, 1), 3)
	try:
		infected = 0
		for user in users:
			infected += 1 if user.version == (1, 1) else 0
		assert infected == 3
		print "SUCCESS"
	except AssertionError:
		print "FAIL"

def test_infection_total():
	"""
	Tests that total_infection infects only the desired maximally-related
	subset of a given graph
	"""

	users = [User() for x in range(0, 6)]
	users[1].add_relationship(users[0], UserRelationship.TEACHER)
	users[1].add_relationship(users[2], UserRelationship.STUDENT)
	users[1].add_relationship(users[3], UserRelationship.BOTH)

	print "test_infection_total: ",
	UserAcademy.total_infection((1, 1), users[0])
	UserAcademy.total_infection((1, 2), users[4])
	try:
		for i in range(0, 4):
			assert users[i].version == (1, 1)
		assert users[4].version == (1, 2)
		assert users[5].version == (1, 0)
		print "SUCCESS"
	except AssertionError:
		print "FAIL"

def test_infection_limited1():
	"""
	Tests that limited_infection infects as close to the given number of
	users as possible (case: target < total)
	"""

	users = _setup_limited_infection()

	print "test_infection_limited (1/3): ",
	academy = UserAcademy(users)
	academy.limited_infection((1, 1), 1)
	try:
		# the algorithm should infect only the single-node
		# component, and nothing else
		assert users[4].version == (1, 1)
		for i in range(0, 4):
			assert users[i].version == (1, 0)
		print "SUCCESS"
	except AssertionError:
		print "FAIL"

def test_infection_limited2():
	"""
	Tests that limited_infection infects as close to the given number of
	users as possible (case: target == total)
	"""

	users = _setup_limited_infection()

	print "test_infection_limited (2/3): ",
	academy = UserAcademy(users)
	academy.limited_infection((1, 1), 5)

	try:
		for user in users:
			assert user.version == (1, 1)
		print "SUCCESS"
	except AssertionError:
		print "FAIL"

def test_infection_limited3():
	"""
	Tests that limited_infection infects as close to the given number of
	users as possible (case: target > total)
	"""

	users = _setup_limited_infection()

	print "test_infection_limited (3/3): ",
	academy = UserAcademy(users)
	academy.limited_infection((1, 1), 6)

	try:
		for user in users:
			assert user.version == (1, 1)
		print "SUCCESS"
	except AssertionError:
		print "FAIL"

def test_infection_enhanced1():
	"""
	Tests that limited_infection_enhanced infects exactly the number of
	users desired (case: subset sum exists)
	"""

	users = _setup_enhanced_infection()

	print "test_infection_enhanced (1/2): ",
	academy = UserAcademy(users)
	academy.limited_infection_enhanced((1, 1), 6)
	try:
		infected = 0
		for classroom in academy._classrooms:
			if classroom.contact.version == (1, 1):
				infected += classroom.size
		assert infected == 6
		print "SUCCESS"
	except AssertionError:
		print "FAIL"

def test_infection_enhanced2():
	"""
	Tests that limited_infection_enhanced infects exactly the number of
	users desired (case: subset sum does not exist)
	"""

	users = _setup_enhanced_infection()

	print "test_infection_enhanced (2/2): ",
	academy = UserAcademy(users)
	academy.limited_infection_enhanced((1, 1), 9)
	try:
		for classroom in academy._classrooms:
			assert classroom.contact.version == (1, 0)
		print "SUCCESS"
	except AssertionError:
		print "FAIL"

def test_all():
	print "Running tests..."
	test_infection_singular()
	test_infection_direct()
	test_infection_indirect()
	test_infection_circular()
	test_infection_limit()

	print
	test_infection_total()

	print
	test_infection_limited1()
	test_infection_limited2()
	test_infection_limited3()

	print
	test_infection_enhanced1()
	test_infection_enhanced2()


print
test_all()
print
