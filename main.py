from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
Bootstrap(app)


@app.route('/')
def index():
    return render_template("index.html")


from views import *

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 8000)

