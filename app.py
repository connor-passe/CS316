from flask import Flask, request, render_template, redirect, url_for, flash, session
#from flask_login import LoginManager, login_user, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request
from wtform_fields import *

app = Flask(__name__)
app.secret_key = 'replace later'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
sessionvar = False
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

meats = ['chicken', 'pork', 'beef', 'turkey', 'duck', 'lamb', 'salmon', 'fish']
dairy = ['milk', 'cream', 'yogurt', 'cheese', 'butter']
nuts = ['peanut', 'almond', 'cashew', 'pecan', 'walnut', 'hazelnut', 'nut', 'pistachio']

def exclude(remove):
	list = set()
	list.update(Recipe.query.all())
	for x in remove:
		temp = set()
		temp.update(Recipe.query.filter(~Recipe.ingredients.contains(x)).all())
		list = list.intersection(temp)
	ids = []
	for x in list:
		ids.append(x.id)
	return ids

no_meat = exclude(meats)
no_eggs = exclude(['egg'])
no_dairy = exclude(dairy)
no_nuts = exclude(nuts)

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
'''
@app.route('/set/')
def set():
	session['key'] = 'value'
	return 'ok'

@app.route('/get/')
def get():
	return session.get('key', 'not set')
'''

@app.route('/')
def home():
	return render_template("main.html")

@app.route('/signup/', methods=['GET', 'POST'])
def index():
	reg_form = RegistrationForm()
	login_form = LoginForm()

	if request.method=='GET':
		#reg_form = RegistrationForm()
		return render_template("index.html", form=reg_form)
	if request.method== 'POST':

		username = reg_form.username.data
		password = reg_form.password.data
		confirm_password = reg_form.confirm_pswd.data
		name = reg_form.name.data
		age = reg_form.age.data
		cooking_skill = reg_form.cooking_skill.data
		vegetarian = reg_form.vegetarian.data
		if vegetarian == 'veg':
			vegetarian = True
		else:
			vegetarian = False
		security_answer = reg_form.sec_question.data

		#check username exists
		user_object = Account.query.filter_by(username=username).first()
		if user_object:
			return render_template("index.html", form=reg_form, message = "This username has already been taken!")

		#check that password is between 4 and 25 characters
		if len(password) < 4 or len(password) > 25:
			return render_template("index.html", form=reg_form, message = "Password must be between 4 and 25 characters!")

		#check if passwords match
		if password != confirm_password:
			return render_template("index.html", form=reg_form, message = "The passwords did not match!")

		#check that username is between 4 and 25 characters
		if len(username) < 4 or len(username) > 25:
			return render_template("index.html", form=reg_form, message = "Username must be between 4 and 25 characters!")

		#check that age is an integer
		if not age:
			age=-1
		else:
			try:
				test_age = int(age)
			except:
				return render_template("index.html", form=reg_form, message = "Please enter a valid integer age")

		#add user to db
		account = Account(username=username, password=password, name=name, age=int(age), cooking_skill=cooking_skill, vegetarian=vegetarian, security_answer=security_answer)
		db.session.add(account)
		db.session.commit()
		return render_template("login.html", form=login_form, message = "Account created!")

@app.route('/recipes/', methods=['GET'])
def handle_recipe():
	if request.method == 'GET':
		ingredient = request.args.get('ingredient', '')
		ingredients = ingredient.split(',')
		time = request.args.get('time', '')
		skill = request.args.get('skill', '')
		vegetarian = request.args.get('vegetarian', '')
		vegan = request.args.get('vegan', '')
		nuts = request.args.get('nuts', '')
		dairy = request.args.get('dairy', '')

		recipe = set()
		recipe.update(Recipe.query.filter(Recipe.ingredients.contains(ingredients[0].strip().lower())).all())
		for i in range(1, len(ingredients)):
			temp = set()
			temp.update(Recipe.query.filter(Recipe.ingredients.contains(ingredients[i].strip().lower())).all())
			recipe = recipe.intersection(temp)

		if time != 'any':
			time_limits = time.split(',')
			start = int(time_limits[0])
			if len(time_limits[1])>0:
				end = int(time_limits[1])
				recipe = [x for x in recipe if x.minutes<=end]
			recipe = [x for x in recipe if x.minutes>start]

		if skill != 'any':
			step_limits = skill.split(',')
			lower = int(step_limits[0])
			if len(step_limits[1])>0:
				upper = int(step_limits[1])
				recipe = [x for x in recipe if x.n_steps<=upper]
			recipe = [x for x in recipe if x.n_steps>lower]

		if vegetarian:
			recipe = [x for x in recipe if x.id in no_meat]
		if vegan:
			recipe = [x for x in recipe if x.id in no_meat and x.id in no_eggs and x.id in no_dairy]
		if nuts:
			recipe = [x for x in recipe if x.id in no_nuts]
		if dairy:
			recipe = [x for x in recipe if x.id in no_dairy]
		return render_template("search-results.html", query=recipe, ingredient=ingredient, total=len(recipe), time=time, skill=skill, vegetarian=vegetarian, vegan=vegan, nuts=nuts, dairy=dairy)

@app.route('/recipes/<id>', methods=['GET'])
def one_recipe(id):
	return render_template("one-recipe.html", query=Recipe.query.get(id))

@app.route('/login/', methods=['GET', 'POST'])
def login():
	#sessionvar = False
	login_form = LoginForm()
	if request.method=='GET':
		if 'account_id' in session:
			sessionvar = True
			return render_template("main.html", message="Logged in!")
		else:
			return render_template("login.html", form=login_form)
	elif request.method=='POST':
		username = login_form.username.data
		password = login_form.password.data
		account = Account.query.filter_by(username=login_form.username.data).first()
		if account:
			if account.password==password:
				session['account_id']=account.id
				session['username'] = username
				session['vegetarian']=account.vegetarian
				sessionvar=True
				return render_template("main.html", message="Logged in!")
			else:
				return render_template("login.html", form=login_form, message = "Incorrect password!")

		else:
			return render_template("login.html", form=login_form, message = "No username found!")

@app.route('/logout/', methods=['GET'])
def logout():
	login_form = LoginForm()
	session.pop('account_id')
	session.pop('username')
	session.pop('vegetarian')
	sessionvar=False
	return render_template("login.html", form=login_form, message = "You have been logged out")

if __name__ == '__main__':
	app.run(debug=True)
