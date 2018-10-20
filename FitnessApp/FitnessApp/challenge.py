#A very rough implementation

import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from FitnessApp.db import get_db
from bson.json_util import dumps
from bson.objectid import ObjectId

from pymongo import MongoClient

rise = Blueprint('rise', __name__, url_prefix='/app') #Create a blueprint to handle things related to challenge objects


@rise.route('/subscribe/<OID>')
def subscribe(OID):
	#add a challenge to a user's challenge list
	mdb_client = MongoClient()
	mdb_users= mdb_client.fitness_app.users
	mdb_users.update({"Username": g.user['username']},{'$push':{"Subscriptions": OID,}})

	#print(mdb_users.find_one({"_id": ObjectId(OID)}))
	return redirect('/auth/profile')





@rise.route('/challenges')
def see_challenges():
	mdb_client = MongoClient()
	mdb_challenges = mdb_client.fitness_app.challenges

	all_challenges = list(mdb_challenges.find())
	print(all_challenges)
	mdb_client.close()
	return render_template('/challenge/challenges.html', challenges = all_challenges)

@rise.route('/create', methods=('GET', 'POST')) #users that are not logged in shouldn't be able to make or submit challenges! Don't let them view this page, check that g.user['id'] exists
def create():

	if g.user is None:
		return redirect('auth/login')
	elif request.method == 'GET':
		render_template('/challenge/create.html')
	

	if request.method == 'POST':

		#Get necessary info

		cname = request.form['challenge_name']
		cdesc = request.form['challenge_description']
		cpoints = request.form['points']


		if cname is None:
			return "fail"
		elif cdesc is None:
			return "fail"
		elif cpoints is None:
			return "fail"
		else:
			mdb_client = MongoClient()
			mdb_challenge = mdb_client.fitness_app.challenges

			c = {
				"Name": cname,
				"Description": cdesc,
				"Points": cpoints,

				"Creator": g.user['username']
				}
			chalid = mdb_challenge.insert_one(c).inserted_id
			mdb_profile = mdb_client.fitness_app.users
			mdb_profile.update({"Username": g.user['username']},{'$push':{"Challenges": str(chalid),}})
			mdb_client.close()

			render_template('/challenge/challenges.html')


	return render_template('/challenge/create.html', results = None)