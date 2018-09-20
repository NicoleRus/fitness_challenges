import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from FitnessApp.db import get_db

auth = Blueprint('auth', __name__, url_prefix='/auth') #create a new blueprint named auth, append "/auth" to associated urls

@auth.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		#A user wants to register!
		username = request.form['username'] #get the username and password from the form post
		password = request.form['password']	
		db = get_db() #get access to the sql db
		error = None

		if not username:
			error = "Username is required!"
		elif not password:
			error = "Password is required!"
		elif db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
			error = "User is already registered!"

		if error is None: #make that new user yeh boit
			db.execute('INSERT INTO user (username, password) VALUES (?,?)', (username, generate_password_hash(password)))
			db.commit()
			return "success" #plain text kicks ass. indicates a user was successfully registered.

	return render_template('auth/register.html')

@auth.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None

		user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
		if user is None:
			error = "Incorrect Username or Password!"
		elif not check_password_hash(user['password'], password):
			error = "Incorrect Username or Password!"

		if error == None:
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('home'))

	return render_template('auth/login.html')


@auth.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')
	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
