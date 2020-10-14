#import os

from flask import Flask, request, render_template
#from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://%s:%s@%s/%s' % (
    # ARGS.dbuser, ARGS.dbpass, ARGS.dbhost, ARGS.dbname
    'user', 'example','db','development'
)

# initialize the database connection
db = SQLAlchemy(app)

# initialize database migration management
#MIGRATE = Migrate(APP, DB)

#from models import *

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100))

@app.route('/')
def hello_world():
    return 'Hello, World!'
