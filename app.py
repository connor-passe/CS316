from flask import Flask, request, render_template, redirect, url_for, flash, session
#from flask_login import LoginManager, login_user, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request
from wtform_fields import *

app = Flask(__name__)
app.secret_key = 'replace later'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://%s:%s@%s/%s' % (
	# ARGS.dbuser, ARGS.dbpass, ARGS.dbhost, ARGS.dbname
	'user', 'example','db','development'
)

db = SQLAlchemy(app)

migrate = Migrate(app,db)

class Recipe(db.Model):
	__tablename__ = 'recipes'

	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	name = db.Column(db.String(100))
	minutes = db.Column(db.Integer)
	n_steps = db.Column(db.Integer)
	steps = db.Column(db.String(10000))
	description = db.Column(db.String(200))
	ingredients = db.Column(db.String(200))

	def __init__(self, name, minutes, n_steps, steps, description, ingredients):
		#self.id = id
		self.name = name
		self.minutes = minutes
		self.n_steps = n_steps
		self.steps = steps
		self.description = description
		self.ingredients = ingredients

class Account(db.Model):
	__tablename__ = 'accounts'

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(25), unique=True, nullable=False)
	password = db.Column(db.String(), nullable=False)
	name = db.Column(db.String())
	age = db.Column(db.Integer)
	cooking_skill = db.Column(db.String())
	vegetarian = db.Column(db.Boolean())
	security_answer = db.Column(db.String(), nullable=False)



	def __init__(self, username, password, name, age, cooking_skill, vegetarian, security_answer):
		#self.id = id
		self.username = username
		self.password = password
		self.name = name
		self.age = age
		self.cooking_skill = cooking_skill
		self.vegetarian = vegetarian
		self.security_answer = security_answer

@app.template_filter('parseList')
def parse_list_filter(s):
	s = s.replace('"', "'")
	splitString = s.split("', '")
	toRemove = ["[", "]", "'"]
	returnList = []
	for x in splitString:
		for i in toRemove:
			x = x.replace(i, '')
		returnList.append(x)
	return returnList

@app.route('/set/')
def set():
	session['key'] = 'value'
	return 'ok'

@app.route('/get/')
def get():
	return session.get('key', 'not set')


@app.route('/')
def home():
	return render_template("main.html")

@app.route('/signup/', methods=['GET', 'POST'])
def index():
	reg_form = RegistrationForm()

	if request.method=='GET':
		#reg_form = RegistrationForm()
		return render_template("index.html", form=reg_form)
	if request.method== 'POST':

		username = reg_form.username.data
		password = reg_form.password.data
		name = reg_form.name.data
		age = reg_form.age.data
		cooking_skill = reg_form.cooking_skill.data
		vegetarian = reg_form.vegetarian.data
		security_answer = reg_form.sec_question.data

		#check username exists
		user_object = Account.query.filter_by(username=username).first()
		if user_object:
			return "Someone has taken this username already!"

		#add user to db
		account = Account(username=username, password=password, name=name, age=int(age), cooking_skill=cooking_skill, vegetarian=False, security_answer=security_answer)
		db.session.add(account)
		db.session.commit()
		return "Inserted into DB!"


@app.route('/recipes/', methods=['GET'])
def handle_recipe():
	if request.method == 'GET':
		ingredient = request.args.get('ingredient', '')
		recipe = Recipe.query.filter(recipes.ingredients.contains(ingredient)).all()
		all_recipes = []
		for x in recipe:
			response = {
				"id": x.id,
				"name": x.name,
				"minutes": x.minutes,
				"n_steps": x.n_steps,
				"description": x.description,
				"ingredients": x.ingredients
			}
			all_recipes.append(response)
		#return {"message": "success", "recipe": all_recipes}
		return render_template("search-results.html", query=recipe, ingredient=ingredient)

@app.route('/recipes/<id>', methods=['GET'])
def one_recipe(id):
	return render_template("one-recipe.html", query=Recipe.query.get(id))
	#goal to show all the info for one recipe

@app.route('/login/', methods=['GET', 'POST'])
def login():

	login_form = LoginForm()
	if request.method=='GET':
		if 'account_id' in session:
			return render_template("main.html", message="logged in!")
		else:
			return render_template("login.html", form=login_form)
	elif request.method=='POST':
		username = login_form.username.data
		password = login_form.password.data
		account = Account.query.filter_by(username=login_form.username.data).first()
		if account:
			if account.password==password:
				session['account_id']=account.id
				return render_template("main.html", message="logged in!")
			else:
				return render_template("login.html", form=login_form, message = "incorrect password!")

		else:
			return render_template("login.html", form=login_form, message = "No username found!")

@app.route('/logout/', methods=['GET'])
def logout():
	login_form = LoginForm()
	session.pop('account_id')
	return render_template("login.html", form=login_form, message = "You have been logged out")



if __name__ == '__main__':
	app.run(debug=True)
