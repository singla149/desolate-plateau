from flask import render_template, session, request, redirect, url_for
import json

from main import app

@app.route('/delete-student/', methods=["GET", "POST"])
def delete_student():
    obj = "Student"
    key = "Roll No"
    if request.method == 'POST':
        students = {}
        print request.form
        with open("files/students.json", "r") as f:
            students = json.load(f)
        enrollments = {}
        with open("files/enrollments.json", "r") as f:
            enrollments = json.load(f)
        roll = request.form[key]

        if roll not in students:
            return "\n\nERROR! No such student exists!\n\n"
        all_removals = []
        for enroll in enrollments:
            if roll == enroll.split("##@@##")[0]:
                removal = [enroll.split("##@@##")[1], enrollments[enroll]["doe"]]
                all_removals.append(removal)

        name = students[roll]["name"]
        if "hidden" not in request.form:
            return render_template("delete.html", obj = obj, keyval = roll,
                                key = key, flag = 2, name = name,
                                key2 = "enrollments", rows = all_removals,
                                cols = ["Course ID", "Date of Enrollment"]
                                )

        print request.form["hidden"]
        if request.form["hidden"] == "0":
            print "ASDASDSAD"
            return redirect(url_for('index'))
        for removal in all_removals:
            del enrollments[roll+"##@@##"+removal[0]]
        del students[roll]
        with open("files/students.json", "w") as f:
            json.dump(students, f)
        with open("files/enrollments.json", "w") as f:
            json.dump(enrollments, f)
        return render_template("delete.html", obj = obj, keyval = roll,
                                flag = 3, name = name,
                                )

    else:
        return render_template("delete.html", obj = obj, key = key, flag = 1)