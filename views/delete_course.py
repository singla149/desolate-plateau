from flask import render_template, session, request, redirect, url_for
import json

from main import app

@app.route('/delete-course/', methods=["GET", "POST"])
def delete_course():
    obj = "Course"
    key = "Course ID"
    if request.method == 'POST':
        courses = {}
        print request.form
        with open("files/courses.json", "r") as f:
            courses = json.load(f)
        enrollments = {}
        with open("files/enrollments.json", "r") as f:
            enrollments = json.load(f)
        c_id = request.form[key]

        if c_id not in courses:
            return "\n\nERROR! No such course exists!\n\n"
        all_removals = []
        for enroll in enrollments:
            if c_id == enroll.split("##@@##")[1]:
                removal = [enroll.split("##@@##")[0], enrollments[enroll]["doe"]]
                all_removals.append(removal)

        name = courses[c_id]["name"]
        if "hidden" not in request.form:
            return render_template("delete.html", obj = obj, keyval = c_id,
                                key = key, flag = 2, name = name,
                                key2 = "enrollments", rows = all_removals,
                                cols = ["Roll No", "Date of Enrollment"]
                                )

        print request.form["hidden"]
        if request.form["hidden"] == "0":
            print "ASDASDSAD"
            return redirect(url_for('index'))
        for removal in all_removals:
            del enrollments[removal[0]+"##@@##"+c_id]
        del courses[c_id]
        with open("files/courses.json", "w") as f:
            json.dump(courses, f)
        with open("files/enrollments.json", "w") as f:
            json.dump(enrollments, f)
        return render_template("delete.html", obj = obj, keyval = c_id,
                                flag = 3, name = name,
                                )

    else:
        return render_template("delete.html", obj = obj, key = key, flag = 1)