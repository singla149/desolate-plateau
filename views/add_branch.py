from flask import render_template, session, flash, request
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange

import json
import datetime

from main import app

class AddBranchForm(Form):
    name = StringField('Name:', render_kw = {"placeholder": "Name"},
        validators= [DataRequired(), Regexp("[a-z.A-Z\s]+$",
            message="Incorrect format, name shouldn't contain any special characters or numbers.")]
        )
    submit =  SubmitField('Add!')

    def validate(self):
        if not Form.validate(self):
            return False
        
        
        _name = self.name.data

        rv = True

        branches = {}
        with open("files/branches.json", "r") as f:
            branches = json.load(f)
        for key in branches:
            if branches[key]["name"] == _name:
                self.name.errors.append(
                    "Branch with this name already exists."
                    )
                rv = False
                break
        return rv

@app.route('/add-branch/', methods =["GET", "POST"])
def add_branch():
    obj = "Branch"

    form = AddBranchForm()
    if form.validate_on_submit():
        branches = {}
        with open("files/branches.json", "r") as f:
            branches = json.load(f)
        
        branches[str(len(branches)+1)] = {
            "name": form.name.data
        }
        with open("files/branches.json", "w") as f:
            json.dump(branches, f)
        
        flash("Branch added successfully.", "success")
        return render_template("add_data.html", form = form, obj = obj)
    elif request.method == "POST":
        flash("There seem to be some errors in the form", "danger")
    return render_template("add_data.html", form = form, obj = obj)