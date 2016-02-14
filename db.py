import validations
import datetime
from tabulate import tabulate

class Student:
	"""Student class"""
	@staticmethod
	def list_students(students, branches):
		all_students = []
		for roll in students:
			stu = students[roll]
			curr = [roll, 
				stu["name"],
				stu["dob"],
				stu["sex"],
				stu["addr"],
				stu["ph_no"],
				branches[stu["b_id"]]["name"],
				stu["c_type"]
			]
			all_students.append(curr)

		print "\n\nStudents in the database:\n\n"
		print tabulate(all_students, 
			headers = ["Roll No.", "Name", "DOB", "Sex", "Address", "Phone No.", "Branch", "Type"], 
			tablefmt = "grid"
			)
		print "\n\n"	

	@staticmethod
	def delete_student(students, enrollments):
		roll = raw_input("Enter roll no. of the student: ")
		if roll not in students:
			print "\n\nERROR! No such student exists!\n\n"
			return
		all_removals = []
		for key in enrollments:
			if roll == key.split("##@@##")[0]:
				removal = [key.split("##@@##")[1], enrollments[key]["doe"]]
				all_removals.append(removal)

		print "\n\nStudent", roll, students[roll]["name"], "removed."

		for removal in all_removals:
			del enrollments[roll+"##@@##"+removal[0]]
		del students[roll]

		print "\n\nRemovals for student:\n\n"
		print tabulate(all_removals, 
			headers = ["Course ID", "Enrollment Date"], 
			tablefmt = "grid"
			)
		print "\n\n"

	@staticmethod
	def modify_student(students):
		roll = raw_input("Enter roll no. of the student: ")
		if roll not in students:
			print "\n\nERROR! Student not registered!\n\n"
			return

		stu = students[roll]
		print "Leave the fields blank to retain old values\n\n"
		print "Current name:", stu["name"]
		name = raw_input("Enter name: ")
		if name != "":
			while not validations.name(name):
				name = raw_input("Enter name: ")
			stu["name"] = name

		print "Current sex:", stu["sex"]
		sex = raw_input("Enter sex: ")
		if sex != "":
			while not validations.sex(sex.upper()):
				sex = raw_input("Enter sex: ")
			stu["sex"] = sex

		print "Current DOB:", stu["dob"]
		dob = raw_input("Enter dob (YYYY-MM-DD): ")
		if dob != "":
			while not validations.date(dob):
				dob = raw_input("Enter dob (YYYY-MM-DD): ")
			stu["dob"] = dob

		print "Current phone number:", stu["ph_no"]
		ph = raw_input("Enter phone number: ")
		if ph != "":
			while not validations.phno(ph):
				ph = raw_input("Enter phone number: ")
			stu["ph_no"] = ph

		addr = raw_input("Enter Address: ")
		if addr != "":
			students[roll]["addr"] = addr

	@staticmethod
	def new_student(students, branches):
		roll = raw_input("Enter roll no.: ")
		while roll == "":
			print "Incorrect format, Roll no. cannot be blank."
			roll = raw_input("Enter roll no.: ")
		name = raw_input("Enter name: ")
		while not validations.name(name):
			name = raw_input("Enter name: ")
		c_type = raw_input("Enter course type (UG/PG): ")
		while not validations.c_type(c_type.upper()):
			c_type = raw_input("Enter course type (UG/PG): ")
		sex = raw_input("Enter sex: ")
		while not validations.sex(sex.upper()):
			sex = raw_input("Enter sex: ")
		dob = raw_input("Enter dob (YYYY-MM-DD): ")
		while not validations.date(dob):
			dob = raw_input("Enter dob (YYYY-MM-DD): ")
		ph = raw_input("Enter phone number: ")
		while not validations.phno(ph):
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
			return
		if roll in students:
			print "\n\nERROR! Student already registered!\n\n"
			return
		students[roll] = {
			"name": name,
			"c_type": c_type,
			"dob": dob,
			"sex": sex.upper(),
			"addr": addr,
			"ph_no": ph,
			"b_id": b_id 
		}

	def __init__(self, rollno, name, sex, dob, ph_no, addr, b_id, c_type):
		self.rollno = rollno
		self.name = name
		self.sex = sex
		self.dob = dob
		self.ph_no = ph_no
		self.addr = addr
		self.b_id = b_id
		self.c_type = c_type

class Course:
	"""Course class"""
	@staticmethod
	def list_courses(courses, branches):
		all_courses = []
		for c_id in courses:
			cou = courses[c_id]
			curr = [c_id, 
				cou["name"],
				branches[cou["b_id"]]["name"],
				cou["cred"],
				cou["c_type"],
				cou["sem"],
			]
			all_courses.append(curr)
		print "\n\nCourses in the database:\n\n"
		print tabulate(all_courses, 
			headers = ["Course ID", "Name", "Branch", "Credits", "Type", "Semester"], 
			tablefmt = "grid"
			)
		print "\n\n"

	@staticmethod
	def new_course(courses, branches):
		c_id = len(courses)+1
		c_type = raw_input("Enter course type: ")
		while not validations.c_type(c_type.upper()):
			c_type = raw_input("Enter course type: ")
		name = raw_input("Enter course name: ")
		while not validations.name(name):
			name = raw_input("Enter course name: ")
		cred = raw_input("Enter credits: ")
		while not validations.cred(cred):
			cred = raw_input("Enter credits: ")
		sem = raw_input("Enter sem: ")
		while not validations.sem(sem, c_type.upper()):
			sem = raw_input("Enter sem: ")
		br = raw_input("Enter branch: ")
		b_id = -1
		for key in branches:
			if branches[key]["name"] == br:
				b_id = key
				break
		if b_id == -1:
			print "\n\nERROR! No such branch exists!\n\n"
		else:
			courses[c_id] = {
			"c_type": c_type.upper(),
			"name": name,
			"b_id": b_id,
			"cred": cred,
			"sem": sem
			}

	@staticmethod
	def delete_course(courses, enrollments):
		c_id = raw_input("Enter course ID: ")
		if c_id not in courses:
			print "\n\nERROR! No such course exists!\n\n"
			return
		all_removals = []
		for key in enrollments:
			if c_id == key.split("##@@##")[1]:
				removal = [key.split("##@@##")[0], enrollments[key]["doe"]]
				all_removals.append(removal)

		print "\n\nCourse", c_id, courses[c_id]["name"], "removed."

		for removal in all_removals:
			del enrollments[removal[0]+"##@@##"+c_id]
		del courses[c_id]

		print "\n\nRemovals for course:\n\n"
		print tabulate(all_removals, 
			headers = ["Roll No", "Enrollment Date"], 
			tablefmt = "grid"
			)
		print "\n\n"

	@staticmethod
	def modify_course(courses):
		c_id = raw_input("Enter course ID: ")
		if c_id not in courses:
			print "\n\nERROR! No such course exists!\n\n"
			return

		cou = courses[c_id]
		print "Leave the fields blank to retain old values\n\n"
		print "Current name:", cou["name"]
		name = raw_input("Enter name: ")
		if name != "":
			while not validations.name(name):
				name = raw_input("Enter name: ")
			cou["name"] = name

		print "Current credits:", cou["cred"]
		cred = raw_input("Enter Credits: ")
		if cred != "":
			while not validations.cred(cred):
				cred = raw_input("Enter Credits: ")
			cou["cred"] = cred


	def __init__(self, c_id, c_type, name, b_id, cred, sem):
		self.c_id = c_id
		self.c_type = c_type
		self.name = name
		self.b_id=b_id
		self.credits = cred
		self.sem = sem

class Enrollment:
	"""Enrollment class"""
	@staticmethod
	def archive_enrollments(enrollments, archived_enrolls):
		pass
		all_removals = []
		for key in enrollments:
			doe = enrollments[key]["doe"]
			doe = datetime.datetime.strptime(doe, '%Y-%m-%d').date()
			if datetime.date.today() - doe >=  datetime.timedelta(weeks=26):
				removal = [key.split("##@@##")[0], key.split("##@@##")[1], enrollments[key]["doe"]]
				all_removals.append(removal)

		for removal in all_removals:
			del enrollments[removal[0]+"##@@##"+removal[1]]
			archived_enrolls[removal[0]+"##@@##"+removal[1]] = {"doe": removal[2]}

		print "\n\nEnrollments that were archived:\n\n"
		print tabulate(all_removals,
			headers = ["Roll No.", "Course ID", "Enrollment Date"],
			tablefmt = "grid"
			)
		print "\n\n"

	@staticmethod
	def new_enrollment(enrollments, students, courses):
		roll = raw_input("Enter roll no.: ")
		if roll not in students:
			print "\n\nERROR! No such student exists!\n\n"
			return

		c_id = raw_input("Enter course id: ")
		if c_id not in courses:
			print "\n\nERROR! No such course exists!\n\n"
			return
		
		c_type = courses[c_id]["c_type"]
		if students[roll]["c_type"] != c_type:
			print "\n\nERROR! Course not available for this student!\n\n"
			return

		b_id = courses[c_id]["b_id"]
		if b_id != students[roll]["b_id"]:
			print "\n\nERROR! Cannot enroll student in other branch's course!\n\n"
			return

		key = roll + "##@@##" + c_id

		if key in enrollments:
			print "\n\nERROR! Student already enrolled for this course!\n\n"
			return
		sem = courses[c_id]["sem"]
		enroll_courses = []
		for c_id in courses:
			if sem == courses[c_id]["sem"] and b_id == courses[c_id]["b_id"] and c_type == courses[c_id]["c_type"]:
				enroll_courses.append( [c_id, courses[c_id]["name"]] )

		for course in enroll_courses:
			key = roll + "##@@##" + course[0]
			if key not in enrollments:
				enrollments[key] = {"doe": str(datetime.date.today())}

		print "\n\nStudent registered successfully for the following courses:\n\n"
		print tabulate(enroll_courses, 
			headers = ["Course ID", "Course Name"], 
			tablefmt = "grid"
			)
		print "\n\n"

	def __init__(self, c_id, rollno, doe):
		self.c_id = c_id
		self.rollno = rollno
		self.doe = doe

class Branch:
	"""Branch class"""
	def __init__(self, b_id, name):
		self.b_id = b_id
		self.name = name
