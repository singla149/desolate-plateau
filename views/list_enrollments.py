from flask import render_template, session, flash, request
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange

import json
import datetime

from main import app

class ListEnrollByCIDForm(Form):
    c_id = SelectField('Course ID:', validators=[DataRequired()])
    submit =  SubmitField('List!')

@app.route('/list-enrollments/course/', methods =["GET", "POST"])
def list_enrolls_by_CID():
    obj = "Course"
    form = ListEnrollByCIDForm()
    courses = {}
    with open("files/courses.json", "r") as f:
        courses = json.load(f)
    form.c_id.choices = [(c_id, str(c_id) + " - " + courses[c_id]["name"]) for c_id in sorted(courses)]

    if form.validate_on_submit():
        enrollments = {}
        with open("files/enrollments.json") as f:
            enrollments = json.load(f)
        archived_enrolls = {}
        with open("files/archived_enrolls.json", "r") as f:
            archived_enrolls = json.load(f)
        students = {}
        with open("files/students.json") as f:
            students = json.load(f)

        current_enrollments = []
        for key in enrollments:
            if form.c_id.data == key.split("##@@##")[1]:
                roll = key.split("##@@##")[0]
                enrol = [roll, students[roll]["name"], enrollments[key]["doe"]]
                current_enrollments.append(enrol)
        prev_enrollments = []
        for key in archived_enrolls:
            if form.c_id.data == key.split("##@@##")[1]:
                roll = key.split("##@@##")[0]
                enrol = [roll, students[roll]["name"], archived_enrolls[key]["doe"]]
                prev_enrollments.append(enrol)

        cols = ["Roll No.", "Name", "Date of Enrollment"]

        return render_template("list_enrollments.html", form = form, obj = obj, cols = cols,
                rows1 = current_enrollments, rows2 = prev_enrollments)
    elif request.method == "POST":
        flash("There seem to be some errors in the form", "danger")
    return render_template("list_enrollments.html", form = form, obj = obj)


class ListEnrollByRollNoForm(Form):
    roll = SelectField('Roll No.:', validators=[DataRequired()])
    submit =  SubmitField('List!')


@app.route('/list-enrollments/student/', methods =["GET", "POST"])
def list_enrolls_by_RollNo():
    obj = "Student"
    form = ListEnrollByRollNoForm()
    students = {}
    with open("files/students.json", "r") as f:
        students = json.load(f)
    form.roll.choices = [(roll, str(roll) + " - " + students[roll]["name"]) for roll in sorted(students)]

    if form.validate_on_submit():
        enrollments = {}
        with open("files/enrollments.json") as f:
            enrollments = json.load(f)
        archived_enrolls = {}
        with open("files/archived_enrolls.json", "r") as f:
            archived_enrolls = json.load(f)
        courses = {}
        with open("files/courses.json") as f:
            courses = json.load(f)

        current_enrollments = []
        for key in enrollments:
            if form.roll.data == key.split("##@@##")[0]:
                c_id = key.split("##@@##")[1]
                enrol = [c_id, courses[c_id]["name"], enrollments[key]["doe"]]
                current_enrollments.append(enrol)
        prev_enrollments = []
        for key in archived_enrolls:
            if form.roll.data == key.split("##@@##")[0]:
                c_id = key.split("##@@##")[1]
                enrol = [c_id, courses[c_id]["name"], archived_enrolls[key]["doe"]]
                prev_enrollments.append(enrol)

        cols = ["Course ID", "Name", "Date of Enrollment"]

        return render_template("list_enrollments.html", form = form, obj = obj, cols = cols,
                rows1 = current_enrollments, rows2 = prev_enrollments)
    elif request.method == "POST":
        flash("There seem to be some errors in the form", "danger")
    return render_template("list_enrollments.html", form = form, obj = obj)
