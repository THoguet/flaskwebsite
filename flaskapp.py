from flask import *
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from makeIcs import  cal
import os
import time
app = Flask(__name__)
app.config['SECRET_KEY'] = '***REMOVED***'
app.secret_key = b"***REMOVED***"
socketio = SocketIO(app, cors_allowed_origins='*')

def exist(tab,test):
	return test in tab

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

@app.route("/getcal/", methods=['GET'])
@app.route("/getcal/<group>", methods=['GET'])
@app.route("/getcal/<group>/", methods=['GET'])
def calUni(group=None):
	if group == None:
		redirect(url_for('quatrecentquatre'))
	try:
		for i in os.listdir("./static/ics/"):
			if i == 'calUni '+group+' '+str(request.args)[20:-2].replace("(","").replace("',",":").replace("'","").replace(")","")+'.ics':
				if (time.time()-int(os.path.getmtime('./static/ics/calUni '+group+' '+str(request.args)[20:-2].replace("(","").replace("',",":").replace("'","").replace(")","")+'.ics'))>21600):
					cal(group,request.args)
					return send_from_directory('./static/ics/', path='calUni '+group+' '+str(request.args)[20:-2].replace("(","").replace("',",":").replace("'","").replace(")","")+'.ics')
				return send_from_directory('./static/ics/', path='calUni '+group+' '+str(request.args)[20:-2].replace("(","").replace("',",":").replace("'","").replace(")","")+'.ics')
		cal(group,request.args)
		return send_from_directory('./static/ics/', path='calUni '+group+' '+str(request.args)[20:-2].replace("(","").replace("',",":").replace("'","").replace(")","")+'.ics')
	except FileNotFoundError:
		abort(404)

@app.route("/yt")
@app.route("/yt/")
def ytgetlink():
	return render_template("ytask.html")

@app.route("/yt/player", methods=['GET', 'POST'])
def yt():
	if exist(request.form,"linkyt") and request.form['linkyt'] != "":
		return redirect(url_for('player',link=str(request.form['linkyt'][32:])))
	return redirect(url_for('ytgetlink'))

@app.route("/yt/player/<link>", methods=['GET', 'POST'])
def player(link):
	return render_template("yt.html", linkyt=link)

@app.route("/admin", methods=['GET', 'POST'])
def admin():
	if 'username' in session:
		return f'Logged in as {session["username"]}'
	return redirect(url_for('login'))

@socketio.on('pause')
def pauseVideo(time,pvid,room,dst,username= "Ano"):
	join_room(room)
	emit('pause', (time,username,pvid,dst), to=room, skip_sid=request.sid)

@socketio.on('play')
def playVideo(time,pvid,room,dst,username= "Ano"):
	join_room(room)
	emit('play', (time,username,pvid,dst), to=room, skip_sid=request.sid)

@socketio.on('join')
def joinroom(room,username="Ano"):
	join_room(room)
	emit('join', username, to=room, skip_sid=request.sid)

@socketio.on('leave')
def leaveroom(room,username="Ano"):
	join_room(room)
	emit('leave', username, to=room, skip_sid=request.sid)
	leave_room(room)

if __name__ == '__main__':
	socketio.run(app, host='0.0.0.0')