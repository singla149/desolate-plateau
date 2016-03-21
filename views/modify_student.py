from flask import render_template, session, flash, request
from flask_wtf import Form
from wtforms import StringField, SubmitField, HiddenField, TextAreaField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange

import json
import datetime

from main import app

class ChooseStudentForm(Form):
    rollno = SelectField('Roll No.:', validators=[DataRequired()])
    submit =  SubmitField('Select!')

class ModifyStudentForm(Form):
    roll = HiddenField("Roll No:")
    name = StringField('Name:', render_kw = {"placeholder": "Name"},
        validators = [DataRequired(),
        Regexp("[a-z.A-Z\s]+$",
            message="Incorrect format, name shouldn't contain any special characters or numbers.")]
        )

    sex = SelectField('Sex:',choices = [('M','Male'),('F','Female'),],
        validators=[DataRequired()]
        )

    # sem = IntegerField('Semester:',  render_kw = {"placeholder": "Semester"},
    #     validators=[DataRequired()]
    #     )

    dob = DateField('Date of Birth:', validators=[DataRequired()])

    doa = DateField('Date of Admission:', validators=[DataRequired()])

    addr = TextAreaField('Address:', render_kw = {"placeholder": "Address"},
        validators=[DataRequired()])

    ph_no = IntegerField('Phone Number:',  render_kw = {"placeholder": "Phone Number"},
        validators=[DataRequired(),
            NumberRange(min=1111111111, max=9999999999, message="Please enter a valid mobile number.")])

    submit =  SubmitField('Modify!')

    def validate(self):
        if not Form.validate(self):
            return False
        
        _roll = self.roll.data
        _dob = self.dob.data
        _doa = self.doa.data
        #_sem = self.sem.data
        students = {}
        with open("files/students.json", "r") as f:
            students = json.load(f)
        _c_type = students[_roll]["c_type"]

        rv = True



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

        # limit = {"UG": 8, "PG": 4}
        # lim = limit[_c_type]
        # if _sem not in xrange(1, lim+1):
        #     self.sem.errors.append(
        #         "Incorrect sem. Should be between 1-" + str(lim) + " for " + _c_type
        #         )
        #     rv = False

        return rv

@app.route('/modify-student/', methods =["GET", "POST"])
def modify_student():
    obj = "Student"
    form1 = ChooseStudentForm()

    students = {}
    with open("files/students.json", "r") as f:
        students = json.load(f)
    form1.rollno.choices = [(roll, str(roll) + " - " + students[roll]["name"]) for roll in sorted(students,key=lambda x: int(x))]

    form2 = ModifyStudentForm()
    if form2.validate_on_submit():
        students = {}
        with open("files/students.json", "r") as f:
            students = json.load(f)

        _roll = str(form2.roll.data)
        students[_roll]["name"] = form2.name.data
        students[_roll]["dob"] = form2.dob.data.strftime("%Y-%m-%d")
        students[_roll]["doa"] = form2.doa.data.strftime("%Y-%m-%d")
        students[_roll]["sex"] = form2.sex.data
        students[_roll]["addr"] = form2.addr.data
        students[_roll]["ph_no"] = form2.ph_no.data
        with open("files/students.json", "w") as f:
            json.dump(students, f)
        flash("Data modified successfully", "success")
        return render_template("modify_data.html", form1 = form1, form2 = form2, obj = obj)

    elif form1.validate_on_submit():
        students = {}
        with open("files/students.json", "r") as f:
            students = json.load(f)
        _roll = form1.rollno.data
        form2 = ModifyStudentForm()
        form2.roll.render_kw = {"value": _roll}
        form2.name.render_kw = {"placeholder": "Name", "value": students[_roll]["name"]}
        form2.sex.render_kw = {"placeholder": "Sex", "value": students[_roll]["sex"]}
        #form2.sem.render_kw = {"placeholder": "Semester", "value": students[_roll]["sem"]}
        form2.dob.render_kw = {"value": students[_roll]["dob"]}
        form2.doa.render_kw = {"value": students[_roll]["doa"]}
        form2.addr.render_kw = {"placeholder": "Address"}
        form2.ph_no.render_kw = {"placeholder": "Phone Number", "value": students[_roll]["ph_no"]}
        flash("Please enter new data for the student.", "info")
        return render_template("modify_data.html", form1 = form1, form2 = form2, obj = obj, addr = students[_roll]["addr"])
    elif request.method == "POST":
        flash("There seem to be some errors in the form", "danger")
        if not form2.validate():
            return render_template("modify_data.html", form1 = form1, form2 = form2, obj = obj)
    return render_template("modify_data.html", form1 = form1, obj = obj)