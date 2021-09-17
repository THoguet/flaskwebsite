from  flask import *
from markupsafe import escape

app = Flask(__name__)
app.secret_key = b"***REMOVED***"

def exist(tab,test):
	for i in tab:
		if test == i:
			return True
	return False

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
	if request.cookies.get('username') != None:
		session['username'] = request.cookies.get('username')
		session['pswd'] = request.cookies.get('pswd')
		return redirect(url_for('admin'))
	elif request.method == 'POST':
		if exist(request.form,"username") and request.form['username'] != "":
			if exist(request.form,"pswd") and request.form['pswd'] != "":
				session['username'] = request.form['username']
				session['pswd'] = request.form['pswd']
				if exist(request.form,"stayconnected"):
					resp = make_response(redirect(url_for('admin')))
					resp.set_cookie('username', session['username'])
					resp.set_cookie('pswd', session['pswd'])
					return resp
				return redirect(url_for('admin'))
	return render_template("login.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route("/404")
def quatrecentquatre():
	return render_template('404.html')

@app.route("/admin", methods=['GET', 'POST'])
def admin():
	if 'username' in session:
		return f'Logged in as {session["username"]}'
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run() 