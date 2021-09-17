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

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('admin'))
    return render_template("login.html")

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return redirect(url_for('login'))

#if __name__ == '__main__':
#    app.run()
