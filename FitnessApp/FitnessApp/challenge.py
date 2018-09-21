import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from FitnessApp.db import get_db

challenge = Blueprint('challenge', __name__, url_prefix='/app') #Create a blueprint to handle things related to challenge objects

@challenge.route('/create', methods=('GET', 'POST'))
def create():

	if request.method == 'POST':
		#put dat sweet form data into some json
		


	return render_template('/challenge/create.html')