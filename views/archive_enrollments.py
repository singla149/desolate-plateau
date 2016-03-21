from flask import render_template, session, flash
import json
import datetime

from main import app

@app.route('/archive-enrollments/')
def archive_enrollments():
    enrollments = {}
    with open("files/enrollments.json", "r") as f:
        enrollments = json.load(f)
    archived_enrolls = {}
    with open("files/archived_enrolls.json", "r") as f:
        archived_enrolls = json.load(f)

    data = []
    for key in enrollments:
        doe = enrollments[key]["doe"]
        doe = datetime.datetime.strptime(doe, '%Y-%m-%d').date()
        if datetime.date.today() - doe >=  datetime.timedelta(weeks=26):
            removal = [key.split("##@@##")[0], key.split("##@@##")[1], enrollments[key]["doe"]]
            data.append(removal)

    for removal in data:
        del enrollments[removal[0]+"##@@##"+removal[1]]
        archived_enrolls[removal[0]+"##@@##"+removal[1]] = {"doe": removal[2]}

    with open("files/enrollments.json", "w") as f:
        json.dump(enrollments, f)
    with open("files/archived_enrolls.json", "w") as f:
        json.dump(archived_enrolls, f)

    rows = data.sort(key=lambda x: x[0])
    col = [("numeric", "Roll No."), ("numeric", "Course ID"), ("input-text", "Enrollment Date")]
    flash("Following are the enrollments newly archived. Enrollments that were more than 6 months old were archived.", "info")
    return render_template('list_data.html', obj = "Newly Archived Enrollments", rows = data, cols = col)