class Student:
	"""Student class"""
	def __init__(self, rollno, name, sex, dob, ph_no, addr):
		self.rollno = rollno
		self.name = name
		self.sex = sex
		self.dob = dob
		self.ph_no = ph_no
		self.addr = addr


class Course:
	"""Course class"""
	def __init__(self, c_id, c_type, name, b_id, cred, sem):
		self.c_id = c_id
		self.c_type = c_type
		self.name = name
		self.b_id=b_id
		self.credits = cred
		self.sem = sem

class Enrollment:
	"""Enrollment class"""
	def __init__(self, c_id, rollno, doe):
		pass
		self.c_id = c_id
		self.rollno = rollno
		self.doe = doe

class Branch:
	"""Enrollment class"""
	def __init__(self, b_id, name):
		pass
		self.b_id = b_id
		self.name = name
