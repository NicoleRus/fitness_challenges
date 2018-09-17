"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FitnessApp import app

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Hey, I went ahead and set up a Visual Studio solution for us with Flask. Check out the templates, how they work with the CSS, and how the views work. Feel free to shoot me a text or a Teams with questions or anything, if anyone has any treouble.'
    )

#authorization stuff