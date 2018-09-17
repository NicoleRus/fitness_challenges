"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

from FitnessApp import db
db.init_app(app)

import FitnessApp.views
