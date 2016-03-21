from flask import render_template, session, flash, request
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange

import json
import datetime

from main import app

class ListByBranchForm(Form):
    b_id = SelectField('Branch:', validators=[DataRequired()])
    submit =  SubmitField('List!')

@app.route('/list-branches/course/', methods =["GET", "POST"])
def list_courses_by_branch():
    obj = "Courses"
    form = ListByBranchForm()
    branches = {}
    with open("files/branches.json", "r") as f:
        branches = json.load(f)
    form.b_id.choices = [(b_id, branches[b_id]["name"]) for b_id in sorted(branches)]

    if form.validate_on_submit():
        courses = {}
        with open("files/courses.json") as f:
            courses = json.load(f)
        branch_courses = []
        for key in courses:
            if form.b_id.data == courses[key]["b_id"]:
                curr = []
                curr.append(key)
                curr.append(courses[key]["name"])
                curr.append(courses[key]["cred"])
                curr.append(courses[key]["c_type"])
                branch_courses.append(curr)

        for x in branch_courses:
            x[0] = int(x[0])
        branch_courses.sort(key=lambda x: x[0])
        cols = [("numeric", "Course ID"), ("input-text", "Name"), 
        ("input-text", "Date of Enrollment"), ("input-text", "Course Type")]

        return render_template("list_by_branch.html", form = form, obj = obj, cols = cols,
                rows = branch_courses)
    elif request.method == "POST":
        flash("There seem to be some errors in the form", "danger")
    return render_template("list_by_branch.html", form = form, obj = obj)


@app.route('/list-branches/student/', methods =["GET", "POST"])
def list_students_by_branch():
    obj = "Students"
    form = ListByBranchForm()
    branches = {}
    with open("files/branches.json", "r") as f:
        branches = json.load(f)
    form.b_id.choices = [(b_id, branches[b_id]["name"]) for b_id in sorted(branches)]

    if form.validate_on_submit():
        students = {}
        with open("files/students.json") as f:
            students = json.load(f)
        branch_students = []
        for key in students:
            if form.b_id.data == students[key]["b_id"]:
                curr = []
                curr.append(key)
                curr.append(students[key]["name"])
                curr.append(students[key]["dob"])
                curr.append(students[key]["doa"])
                curr.append(students[key]["ph_no"])
                curr.append(students[key]["sex"])
                curr.append(students[key]["c_type"])
                branch_students.append(curr)

        for x in branch_students:
            x[0] = int(x[0])
        branch_students.sort(key=lambda x: x[0])
        cols = [("numeric", "Roll No."), ("input-text", "Name"), ("input-text", "Date of Birth"),
         ("input-text", "Date of Admission"), ("numeric", "Phone No."), ("input-text", "Sex"),
          ("input-text", "Course Type")]
        return render_template("list_by_branch.html", form = form, obj = obj, cols = cols,
                rows = branch_students)
    elif request.method == "POST":
        flash("There seem to be some errors in the form", "danger")
    return render_template("list_by_branch.html", form = form, obj = obj)
