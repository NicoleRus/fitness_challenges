import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from FitnessApp.db import get_db

auth = Blueprint('auth', __name__, url_prefix='/auth') #create a new blueprint named auth, append "/auth" to associated urls

