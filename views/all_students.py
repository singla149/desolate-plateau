from flask import render_template, session
import json

from main import app

@app.route('/all-students/')
def all_students():
    students = {}
    with open("files/students.json", "r") as f:
        students = json.load(f)
    with open("files/branches.json", "r") as f:
        branches = json.load(f)
    data = []
    for roll in sorted(students):
        stu = students[roll]
        curr = [roll, 
            stu["name"],
            stu["dob"],
            stu["doa"],
            stu["sex"],
            stu["addr"],
            stu["ph_no"],
            branches[stu["b_id"]]["name"],
            stu["c_type"]
        ]
        data.append(curr)

    for x in data:
        x[0] = int(x[0])
    
    data.sort(key=lambda x: x[0])
    col = [("numeric", "Roll No."), ("input-text", "Name"), ("input-text", "Date Of Birth"),
     ("input-text", "Date Of Admission"), ("input-text", "Sex"), ("input-text", "Address"),
      ("numeric", "Phone No."), ("input-text", "Branch"), ("input-text", "Course type")]
    return render_template('list_data.html', obj = "Students", rows = data, cols = col)