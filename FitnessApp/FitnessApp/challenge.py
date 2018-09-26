#A very rough implementation

import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from FitnessApp.db import get_db
from bson.json_util import dumps
from pymongo import MongoClient
from bson import json_util
rise = Blueprint('rise', __name__, url_prefix='/app') #Create a blueprint to handle things related to challenge objects

client = MongoClient()

mdb = client.fitness_app
challenges = mdb.challenges

@rise.route('/challenges')
def see_challenges():
	user_challenges = list(challenges.find({'submitter': str(g.user['id'])})) #should return the user's submitted challenges
	all_challenges = list(challenges.find())
	#dumps(user_challenges)
	return render_template('/challenge/challenges.html', yours = user_challenges, theirs = all_challenges)

@rise.route('/create', methods=('GET', 'POST')) #users that are not logged in shouldn't be able to make or submit challenges! Don't let them view this page, check that g.user['id'] exists
def create():
	if request.method == 'POST':
		error = None
		#put dat sweet form data into some json
		if request.form['challenge_name'] is "":
			error = "Name of Challenge is required!"
		elif request.form['points'] is "":
			error = "Points are required!"
		else:
			if request.form['challenge_description'] is None:
				description = "No Description Available"
			else:
				description = request.form['challenge_description']
			name = request.form['challenge_name']
			points = request.form['points']
			creator = g.user['username']

			c = {
					"name": name,
					"description": description,
					"points": points,
					"submitter": str(g.user['id']),
				}
			challenge_id = challenges.insert_one(c).inserted_id
			print("challenge id = " + str(challenge_id))



			render_template('/challenge/create.html', results=c)


	return render_template('/challenge/create.html', results = None)