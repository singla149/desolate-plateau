from flask import render_template, session, flash, request
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange

import json
import datetime

from main import app

class AddCourseForm(Form):
    c_id = IntegerField('Course ID:', validators=[DataRequired(message="Course ID should be a valid number.")])
    name = StringField('Name:', validators=
        [DataRequired(), 
        Regexp("[a-z.A-Z\s]+$",
            message="Incorrect format, name shouldn't contain any special characters or numbers.")]
        )
    br = SelectField('Branch:', validators=[DataRequired()])
    sem = IntegerField('Semester:', validators=[DataRequired()])
    cred = IntegerField('Credits:', validators=[DataRequired()])
    c_type = SelectField('Course Type:', validators=[DataRequired()])
    submit =  SubmitField('Add!')

    def validate(self):
        if not Form.validate(self):
            return False
        
        _c_id = self.c_id.data
        _c_type = self.c_type.data
        _sem = self.sem.data
        _cred = self.cred.data

        rv = True

        courses = {}
        with open("files/courses.json", "r") as f:
            courses = json.load(f)
        if str(_c_id) in courses:
            self.c_id.errors.append(
                "Course already registered."
                )
            rv = False

        limit = {"UG": 8, "PG": 4}
        lim = limit[_c_type]
        if _sem not in xrange(1, lim+1):
            self.sem.errors.append(
                "Incorrect sem. Should be between 1-" + str(lim) + " for " + _c_type
                )
            rv = False

        if _cred not in xrange(1, 5):
            self.cred.errors.append(
                "Incorrect credits, should be between 1 and 4 only."
                )
            rv = False

        return rv

@app.route('/add-course/', methods =["GET", "POST"])
def add_course():
    obj = "Course"

    form = AddCourseForm()
    branches = {}

    form.c_type.choices = [('UG','UG'),('PG','PG'),]
    with open("files/branches.json", "r") as f:
        branches = json.load(f)
    form.br.choices = [(key, branches[key]["name"]) for key in sorted(branches)]

    if form.validate_on_submit():
        courses = {}
        with open("files/courses.json", "r") as f:
            courses = json.load(f)

        courses[form.c_id.data] = {
        "c_type": form.c_type.data,
        "name": form.name.data,
        "b_id": form.br.data,
        "cred": form.cred.data,
        "sem": form.sem.data
        }
        with open("files/courses.json", "w") as f:
            json.dump(courses, f)
        flash("Course added successfully.", "success")
        return render_template("add_data.html", form = form, obj = obj)
    elif request.method == "POST":
        flash("There seem to be some errors in the form", "danger")
    return render_template("add_data.html", form = form, obj = obj)