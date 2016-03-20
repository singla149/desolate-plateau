from flask import render_template, session, flash, request
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange

import json
import datetime

from main import app

class AddStudentForm(Form):
    roll = IntegerField('Roll No.:', validators=[DataRequired(message="Roll No should be a valid number.")])

    name = StringField('Name:', validators=
        [DataRequired(), 
        Regexp("[a-z.A-Z\s]+$",
            message="Incorrect format, name shouldn't contain any special characters or numbers.")]
        )

    sex = SelectField('Sex:', validators=[DataRequired()])

    c_type = SelectField('Course Type:', validators=[DataRequired()])

    sem = IntegerField('Semester:', validators=[DataRequired()])

    dob = DateField('Date of Birth:', validators=[DataRequired()])

    doa = DateField('Date of Admission:', validators=[DataRequired()])

    br = SelectField('Branch:', validators=[DataRequired()])

    addr = TextAreaField('Address:', validators=[DataRequired()])

    ph_no = IntegerField('Phone Number:', validators=[DataRequired(),
                NumberRange(min=1111111111, max=9999999999, message="Please enter a valid mobile number.")])

    submit =  SubmitField('Add!')

    def validate(self):
        if not Form.validate(self):
            return False
        
        _roll = self.roll.data
        _dob = self.dob.data
        _doa = self.doa.data
        _c_type = self.c_type.data
        _sem = self.sem.data

        rv = True

        students = {}
        with open("files/students.json", "r") as f:
            students = json.load(f)
        if str(_roll) in students:
            self.roll.errors.append(
                "Student already registered."
                )
            rv = False


        ch = {"PG": [21, 30], "UG": [17, 26]}
        if _dob + datetime.timedelta(weeks=52*ch[_c_type][0]) <= _doa:
            if _dob + datetime.timedelta(weeks=52*ch[_c_type][1]) > _doa:
                pass
            else:
                self.dob.errors.append(
                    "Student should be no more than " + str(ch[_c_type][1]) + " years old at the time of admission for " + _c_type + " course."
                    )
                self.doa.errors.append(
                    "Student should be no more than " + str(ch[_c_type][1]) + " years old at the time of admission for " + _c_type + " course."
                    )
                rv = False
        else:
            self.dob.errors.append(
                "Student should be atleast " + str(ch[_c_type][0]) + " years old at the time of admission for " + _c_type + " course."
                )
            self.doa.errors.append(
                "Student should be atleast " + str(ch[_c_type][0]) + " years old at the time of admission for " + _c_type + " course."
                )
            rv = False

        limit = {"UG": 8, "PG": 4}
        lim = limit[_c_type]
        if _sem not in xrange(1, lim+1):
            self.sem.errors.append(
                "Incorrect sem. Should be between 1-" + str(lim) + " for " + _c_type
                )
            rv = False

        return rv

@app.route('/add-student/', methods =["GET", "POST"])
def add_student():
    obj = "Student"
    form = AddStudentForm()

    branches = {}
    form.c_type.choices = [('UG','UG'),('PG','PG'),]
    form.sex.choices = [('M','Male'),('F','Female'),]
    with open("files/branches.json", "r") as f:
        branches = json.load(f)
    form.br.choices = [(key, branches[key]["name"]) for key in sorted(branches)]

    if form.validate_on_submit():
        students = {}
        with open("files/students.json", "r") as f:
            students = json.load(f)
        students[str(form.roll.data)] = {
            "name": form.name.data,
            "c_type": form.c_type.data,
            "dob": form.dob.data.strftime("%Y-%m-%d"),
            "doa": form.doa.data.strftime("%Y-%m-%d"),
            "sex": form.sex.data,
            "addr": form.addr.data,
            "ph_no": form.ph_no.data,
            "b_id": form.br.data 
        }
        with open("files/students.json", "w") as f:
            json.dump(students, f)
        flash("Student added successfully.", "success")
        return render_template("add_data.html", form = form, obj = obj)
    elif request.method == "POST":
        flash("There seem to be some errors in the form", "danger")
    return render_template("add_data.html", form = form, obj = obj)