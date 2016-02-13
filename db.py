class Student:
	"""Student class"""
	@staticmethod
	def new_student(students, branches):
		roll = raw_input("Enter roll no.: ")
		name = raw_input("Enter name: ")
		sex = raw_input("Enter sex: ")
		dob = raw_input("Enter dob (YYYY-MM-DD): ")
		ph = raw_input("Enter phone number: ")
		addr = raw_input("Enter Address: ")
		br = raw_input("Enter branch: ")
		b_id = -1
		for key in branches:
			if branches[key]["name"] == br:
				b_id = key
				break
		if b_id == -1:
			print "\n\nERROR! No such branch exists!\n\n"
		else:
			stu = Student(roll, name, sex, dob, ph, addr, b_id)
			if roll not in students:
				students[roll] = {
					"name": name,
					"dob": sex,
					"sex": sex,
					"addr": addr,
					"ph_no": ph,
					"b_id": b_id
				}
			else:
				print "\n\nERROR! Student already registered!\n\n"

	def __init__(self, rollno, name, sex, dob, ph_no, addr, b_id):
		self.rollno = rollno
		self.name = name
		self.sex = sex
		self.dob = dob
		self.ph_no = ph_no
		self.addr = addr
		self.b_id = b_id


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
		self.c_id = c_id
		self.rollno = rollno
		self.doe = doe

class Branch:
	"""Branch class"""
	def __init__(self, b_id, name):
		self.b_id = b_id
		self.name = name
