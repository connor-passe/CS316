from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request

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
    password = db.Column(db.String(15))
    name = db.Column(db.String(30))
    minutes = db.Column(db.Integer)
    n_steps = db.Column(db.Integer)

    def __init__(self, id, password, name, minutes, n_steps):
        self.id = id
        self.password = password
        self.name = name
        self.minutes = minutes
        self.n_steps = n_steps

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

@app.route('/')
def hello_world():
    return render_template("main.html")

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
        #if vegetarian:
            # need loop through list of common meats and query for recipes that don't contain these and intersect recipe set
            # probably want to write a function to do the exclusion given a list
        #if vegan:
            # exclude eggs, dairy
        #if nuts:
            # exclude nuts
        #if dairy:
            # exclude dairy
        recipe.update(recipes.query.filter(recipes.ingredients.contains(ingredients[0].strip())).all())
        for i in range(1, len(ingredients)):
            temp = set()
            temp.update(recipes.query.filter(recipes.ingredients.contains(ingredients[i].strip())).all())
            recipe = recipe.intersection(temp)

        return render_template("search-results.html", query=recipe, ingredient=ingredient)

@app.route('/recipes/<id>', methods=['GET'])
def one_recipe(id):
    return render_template("one-recipe.html", query=recipes.query.get(id))
    #goal to show all the info for one recipe

if __name__ == '__main__':
    app.run(debug=True)
