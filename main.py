from flask import Flask, render_template
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 8000)

