import json
import datetime
from db import Student, Course, Enrollment, Branch


students = {}
courses = {}
enrollments = {}
branches = {}

def init():
	global students
	global courses
	global enrollments
	global branches 
	with open("files/branches.json", "r") as f:
		branches = json.load(f)
	with open("files/students.json", "r") as f:
		students = json.load(f)
	with open("files/courses.json", "r") as f:
		courses = json.load(f)
	with open("files/enrollments.json", "r") as f:
		enrollments = json.load(f)

def save():
	with open("files/branches.json", "w") as f:
		json.dump(branches, f)
	with open("files/students.json", "w") as f:
		json.dump(students, f)
	with open("files/courses.json", "w") as f:
		json.dump(courses, f)
	with open("files/enrollments.json", "w") as f:
		json.dump(enrollments, f)



def menu():
	print "Welcome!"
	while True:
		print "1.Add a Student"
		print "2.Delete a Student"
		print "3. Look Up Student Record"
		print "4. Add a course"
		print "5. Enroll student in course"
		print "6.Exit"
		ch = raw_input("What would you like to do? ")
		if ch == "1":
			Student.new_student(students, branches)
		elif ch == "2":
			pass
		elif ch == "3":
			pass
		elif ch == "4":
			Course.new_course(courses, branches)
		elif ch == "5":
			Enrollment.new_enrollment(enrollments, students, courses)
		elif ch == "6":
			print "\nBye!\n"
			break
		else:
			print "\nNot Valid Choice! Try again!\n"
		save()

if __name__ == "__main__":
	init()
	menu()
