from flask import Flask, request, render_template, redirect, url_for, flash
#from flask_login import LoginManager, login_user, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request
from wtform_fields import *

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://%s:%s@%s/%s' % (
    # ARGS.dbuser, ARGS.dbpass, ARGS.dbhost, ARGS.dbname
    'user', 'example','db','development'
)

db = SQLAlchemy(app)

migrate = Migrate(app,db)

class recipes(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    minutes = db.Column(db.Integer)
    n_steps = db.Column(db.Integer)
    steps = db.Column(db.String(10000))
    description = db.Column(db.String(200))
    ingredients = db.Column(db.String(200))

    def __init__(self, id, name, minutes, n_steps, steps, description, ingredients):
        self.id = id
        self.name = name
        self.minutes = minutes
        self.n_steps = n_steps
        self.steps = steps
        self.description = description
        self.ingredients = ingredients

class accounts(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String())
    age = db.Column(db.Integer)
    cooking_skill = db.Column(db.String())
    vegetarian = db.Column(db.Boolean())
    security_answer = db.Column(db.String(), nullable=False)



    def __init__(self, id, username, password, name, age, cooking_skill,vegetarian,security_answer):
        self.id = id
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
'''
@app.route('/')
def hello_world():
    return render_template("main.html")
'''
@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()

    # Update database if validation success
    '''
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Hash password
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Add username & hashed password to DB
        user = User(username=username, hashed_pswd=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))
	'''
    return render_template("index.html", form=reg_form)

@app.route('/recipes/', methods=['GET'])
def handle_recipe():
    if request.method == 'GET':
        ingredient = request.args.get('ingredient', '')
        recipe = recipes.query.filter(recipes.ingredients.contains(ingredient)).all()
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
    return render_template("one-recipe.html", query=recipes.query.get(id))
    #goal to show all the info for one recipe

@app.route("/accounts/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()

    # Update database if validation success
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Hash password
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Add username & hashed password to DB
        user = User(username=username, hashed_pswd=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)


@app.route("/login/", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)


@app.route("/logout/", methods=['GET'])
def logout():

    # Logout user
    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
