"""
The flask application package.
"""
import os
from . import db
from flask import Flask
def create_app():
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(DATABASE=os.path.join(app.instance_path, "FitnessApp.sqlite"),SECRET_KEY="password",)
	db.init_app(app)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	from . import auth
	app.register_blueprint(auth.auth)
	from . import challenge
	app.register_blueprint(challenge.rise)
	return app

app = create_app()

import FitnessApp.views
