import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from FitnessApp.db import get_db
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util



auth = Blueprint('auth', __name__, url_prefix='/auth') #create a new blueprint named auth, append "/auth" to associated urls

@auth.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		#A user wants to register!
		username = request.form['username'] #get the username and password from the form post
		password = request.form['password']	
		db = get_db() #get access to the sql db
		mdb_client = MongoClient()
		mdb = mdb_client.fitness_app #get the database from the mongodb client
		mdb_users = mdb.users

		error = None

		if not username:
			error = "Username is required!"
		elif not password:
			error = "Password is required!"
		elif db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
			error = "User is already registered!"

		if error is None: #make that new user yeh boit
			db.execute('INSERT INTO user (username, password) VALUES (?,?)', (username, generate_password_hash(password)))
			
			u = {
				"Username": username,
				"email": request.form['email'],
				"first_name": request.form['first_name'],
				"last_name": request.form['last_name'],
				}
			mdb_users.insert_one(u).inserted_id
			mdb_client.close()
			db.commit()
			return redirect(url_for('auth.show_profile')) #plain text kicks ass. indicates a user was successfully registered.

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
			return redirect(url_for('auth.show_profile'))

	return render_template('auth/login.html')


@auth.route('/profile')
def show_profile():
	if g.user is None:
		return redirect('auth/login')
	else:
		print("are we getting here?")

		#need to get and format:
		#users_subscriptions
		#completed challenges
		#user_created_challenged


		#replace this with get_userprofile, get user profile by ID
		user_profile = get_profile(g.user['username'])
		mdb_client = MongoClient()
		mdb_challenge = mdb_client.fitness_app.challenges
		if 'Subscriptions' in user_profile:
			for x in user_profile['Subscriptions']:
				user_profile['Subscriptions'].remove(x)
				x = mdb_challenge.find_one(ObjectId(x))
				user_profile['Subscriptions'].insert(0, x)

		if 'Challenges' in user_profile:
			for x in user_profile['Challenges']:
				user_profile['Challenges'].remove(x)
				x = mdb_challenge.find_one(ObjectId(x))
				user_profile['Challenges'].insert(0, x)

		print(user_profile)
		return render_template('auth/profile.html', user_profile = user_profile)

@auth.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('auth.login'))

@auth.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')
	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()


def get_profile(username):
	mdb_client = MongoClient()
	mdb_profile = mdb_client.fitness_app.users
	profile = mdb_profile.find_one({"Username":username})
	print(profile)
	mdb_client.close()
	return profile