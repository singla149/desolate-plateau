from flask import render_template, session
import json

from main import app

@app.route('/all-students/')
def all_students():
    students = {}
    with open("files/students.json", "r") as f:
        students = json.load(f)
    print students
    return "HELLO WORLD!"