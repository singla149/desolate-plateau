from flask import render_template, session
import json

from main import app

@app.route('/all-courses/')
def all_courses():
    courses = {}
    with open("files/courses.json", "r") as f:
        courses = json.load(f)
    with open("files/branches.json", "r") as f:
        branches = json.load(f)
    data = []
    for c_id in sorted(courses):
        cou = courses[c_id]
        curr = [c_id, 
            cou["name"],
            branches[cou["b_id"]]["name"],
            cou["cred"],
            cou["c_type"],
            cou["sem"],
        ]
        data.append(curr)
    col = ["Course ID", "Name", "Branch", "Credits", "Type", "Sem"]
    return render_template('list_data.html', obj = "courses", rows = data, cols = col)