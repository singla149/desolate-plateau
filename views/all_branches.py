from flask import render_template, session
import json

from main import app

@app.route('/all-branches/')
def all_branches():
    branches = {}
    with open("files/branches.json", "r") as f:
        branches = json.load(f)
    data = []
    for b_id in sorted(branches):
        cou = branches[b_id]
        curr = [b_id, 
            cou["name"],
        ]
        data.append(curr)
    col = ["Branch ID", "Name"]
    return render_template('list_data.html', obj = "branches", rows = data, cols = col)