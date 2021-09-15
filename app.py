from  flask import *
from markupsafe import escape

app = Flask(__name__)
app.secret_key = b"***REMOVED***"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ts")
def ts():
    return render_template("ts.html")

@app.route("/twitch")
def twitch():
    return render_template("twitch.html")

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"