"""
The flask application package.
"""
import os
from . import db
from flask import Flask
def create_app():
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(DATABASE=os.path.join(app.instance_path, "FitnessApp.sqlite"),)
	db.init_app(app)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass


	return app

app = create_app()

import FitnessApp.views
