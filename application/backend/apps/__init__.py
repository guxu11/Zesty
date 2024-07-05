from flask import Flask
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

load_dotenv(override=True)

# create a Flask application
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# app.debug = True


CORS(app)


# creates an instance of SQLAlchemy and binds it to the Flask application. 
# This allows you to define database models and interact with the database 
# using SQLAlchemy.
db = SQLAlchemy(app)

import apps.router
