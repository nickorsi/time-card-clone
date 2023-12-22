import os #---> When using SQL Alchmey

from models import db, connect_db #---> When using SQL Alchemy


from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension  #---> Debugger tool

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False #---> Switch for redirect pause page, False=off True=on
app.debug = True #---> Switch for debug toolbar, False=off True=on

debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "[DATABASE_URL]", 'postgresql:///timecard_clone')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #---> When using SQL Alchemy
app.config['SQLALCHEMY_ECHO'] = True #---> When using SQL Alchemy

connect_db(app) #---> When using SQL Alchemy