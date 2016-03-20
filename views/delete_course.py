from flask import render_template, session, request, redirect, url_for
import json

from main import app

@app.route('/delete-course/', methods=["GET", "POST"])
def delete_course():
    obj = "Course"
    key = "Course ID"
    if request.method == 'POST':
        courses = {}
        with open("files/courses.json", "r") as f:
            courses = json.load(f)
        enrollments = {}
        with open("files/enrollments.json", "r") as f:
            enrollments = json.load(f)
        c_id = request.form[key]
        archived_enrolls = {}
        with open("files/archived_enrolls.json", "r") as f:
            archived_enrolls = json.load(f)

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

        if request.form["hidden"] == "0":
            return redirect(url_for('index'))
        for removal in all_removals:
            del enrollments[removal[0]+"##@@##"+c_id]
        all_removals = []
        for enroll in archived_enrolls:
            if c_id == enroll.split("##@@##")[1]:
                removal = [enroll.split("##@@##")[0], archived_enrolls[enroll]["doe"]]
                all_removals.append(removal)
        for removal in all_removals:
            del archived_enrolls[removal[0]+"##@@##"+c_id]
        del courses[c_id]
        with open("files/courses.json", "w") as f:
            json.dump(courses, f)
        with open("files/enrollments.json", "w") as f:
            json.dump(enrollments, f)
        with open("files/archived_enrolls.json", "w") as f:
            json.dump(archived_enrolls, f)
        return render_template("delete.html", obj = obj, keyval = c_id,
                                flag = 3, name = name,
                                )

    else:
        return render_template("delete.html", obj = obj, key = key, flag = 1)