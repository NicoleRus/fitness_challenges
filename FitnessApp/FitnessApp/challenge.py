import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from FitnessApp.db import get_db
import json
from pymongo import MongoClient
rise = Blueprint('rise', __name__, url_prefix='/app') #Create a blueprint to handle things related to challenge objects

client = MongoClient()

mdb = client.fitness_app
challenges = mdb.challenges

@rise.route('/create', methods=('GET', 'POST'))
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
				}
			challenge_id = challenges.insert_one(c).inserted_id
			print("challenge id = " + str(challenge_id))


			render_template('/challenge/create.html', results=c)


	return render_template('/challenge/create.html', results = None)