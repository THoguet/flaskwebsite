from  flask import *
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")
@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"