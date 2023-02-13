from flask import *
from makeIcs import cal
import os
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '***REMOVED***'
app.secret_key = b"***REMOVED***"


def exist(tab, test):
	return test in tab


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/ts")
def ts():
	return render_template("ts.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.cookies.get('username') != None:
		session['username'] = request.cookies.get('username')
		session['pswd'] = request.cookies.get('pswd')
		return redirect(url_for('admin'))
	elif request.method == 'POST':
		if exist(request.form, "username") and request.form['username'] != "":
			if exist(request.form, "pswd") and request.form['pswd'] != "":
				session['username'] = request.form['username']
				session['pswd'] = request.form['pswd']
				if exist(request.form, "stayconnected"):
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


@app.route("/getcal/", methods=['GET'])
@app.route("/getcal/<group>", methods=['GET'])
@app.route("/getcal/<group>/", methods=['GET'])
def calUni(group=None):
	if group == None:
		return redirect(url_for('quatrecentquatre'))
	try:
		for i in os.listdir("/var/www/html/static/ics/"):
			if i == 'calUni ' + group + ' ' + str(request.args)[20:-2].replace("(", "").replace(" ", "_").replace("',", ":").replace("'", "").replace(
			    ")", "") + '.ics':
				if (time.time() - int(
				    os.path.getmtime('/var/www/html/static/ics/calUni ' + group + ' ' +
				                     str(request.args)[20:-2].replace("(", "").replace(" ", "_").replace("',", ":").replace("'", "").replace(")", "") + '.ics'))
				    > 21600):
					cal(group, request.args)
					return send_from_directory(
					    '/var/www/html/static/ics/',
					    path='calUni ' + group + ' ' +
					    str(request.args)[20:-2].replace("(", "").replace(" ", "_").replace("',", ":").replace("'", "").replace(")", "") + '.ics')
				return send_from_directory('/var/www/html/static/ics/',
				                           path='calUni ' + group + ' ' +
				                           str(request.args)[20:-2].replace("(", "").replace(" ", "_").replace("',", ":").replace("'", "").replace(")", "") +
				                           '.ics')
		print(group, request.args)
		cal(group, request.args)
		return send_from_directory('/var/www/html/static/ics/',
		                           path='calUni ' + group + ' ' +
		                           str(request.args)[20:-2].replace("(", "").replace(" ", "_").replace("',", ":").replace("'", "").replace(")", "") + '.ics')
	except FileNotFoundError:
		abort(404)


@app.route("/admin", methods=['GET', 'POST'])
def admin():
	if 'username' in session:
		return f'Logged in as {session["username"]}'
	return redirect(url_for('login'))


if __name__ == '__main__':
	app.run()