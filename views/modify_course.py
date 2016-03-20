from flask import render_template, session, flash, request
from flask_wtf import Form
from wtforms import StringField, SubmitField, HiddenField, TextAreaField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange

import json
import datetime

from main import app

class ChooseCourseForm(Form):
    course_id = SelectField('Course ID:', validators=[DataRequired()])
    submit =  SubmitField('Select!')

class ModifyCourseForm(Form):
    c_id = HiddenField('Course ID:')
    name = StringField('Name:', render_kw = {"placeholder": "Name"},
        validators= [DataRequired(), Regexp("[a-z.A-Z\s]+$",
            message="Incorrect format, name shouldn't contain any special characters or numbers.")]
        )
    cred = IntegerField('Credits:', render_kw = {"placeholder": "Credits"}, validators=[DataRequired()])
    submit =  SubmitField('Modify!')

    def validate(self):
        if not Form.validate(self):
            return False
        
        _c_id = self.c_id.data
        _cred = self.cred.data

        rv = True

        if _cred not in xrange(1, 5):
            self.cred.errors.append(
                "Incorrect credits, should be between 1 and 4 only."
                )
            rv = False

        return rv

@app.route('/modify-course/', methods =["GET", "POST"])
def modify_course():
    obj = "Course"
    form1 = ChooseCourseForm()

    courses = {}
    with open("files/courses.json", "r") as f:
        courses = json.load(f)
    form1.course_id.choices = [(c_id, str(c_id) + " - " + courses[c_id]["name"]) for c_id in sorted(courses)]

    form2 = ModifyCourseForm()
    if form2.validate_on_submit():
        courses = {}
        with open("files/courses.json", "r") as f:
            courses = json.load(f)

        _c_id = str(form2.c_id.data)
        courses[_c_id]["name"] = form2.name.data
        courses[_c_id]["cred"] = form2.cred.data
        with open("files/courses.json", "w") as f:
            json.dump(courses, f)
        flash("Data modified successfully", "success")
        return render_template("modify_data.html", form1 = form1, form2 = form2, obj = obj)

    elif form1.validate_on_submit():
        courses = {}
        with open("files/courses.json", "r") as f:
            courses = json.load(f)
        _c_id = form1.course_id.data
        form2 = ModifyCourseForm()
        form2.c_id.render_kw = {"value": _c_id}
        form2.name.render_kw = {"placeholder": "Name", "value": courses[_c_id]["name"]}
        form2.cred.render_kw = {"placeholder": "Credits", "value": courses[_c_id]["cred"]}
        flash("Please enter new data for the student.", "info")
        return render_template("modify_data.html", form1 = form1, form2 = form2, obj = obj)
    elif request.method == "POST":
        flash("There seem to be some errors in the form", "danger")
        if not form2.validate():
            return render_template("modify_data.html", form1 = form1, form2 = form2, obj = obj)
    return render_template("modify_data.html", form1 = form1, obj = obj)