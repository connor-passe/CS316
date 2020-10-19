from flask import Flask, request, render_template
#from flask_migrate import Migrate
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
	description = db.Column(db.String(200))
	ingredients = db.Column(db.String(200))

	def __init__(self, id, name, minutes, n_steps, description, ingredients):
		self.id = id
		self.name = name
		self.n_steps = n_steps
		self.description=description
		self.ingredients=ingredients



@app.route('/')
def hello_world():
	return render_template("ID.html", query=recipes.query.all())

@app.route('/recipes/', methods=['GET'])
def handle_recipe():

    if request.method == 'GET':
        ingredient = request.args.get('ingredient', '')
        recipe = recipes.query.filter(recipes.ingredients.contains(ingredient)).all()
        all_recipes = []
        for x in recipe:
            response = {
                "name": x.name,
                "minutes": x.minutes,
                "n_steps": x.n_steps,
    			"description": x.description,
                "ingredients": x.ingredients
            }
            all_recipes.append(response)
        return {"message": "success", "recipe": all_recipes}

if __name__ == '__main__':
    app.run(debug=True)
