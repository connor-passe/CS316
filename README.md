# CS316 Final Project: Recipe By ingredients

### Team Members
* Selena Qian - set up and deployment, search functionality, styling
* Nicole Patterson
* Nikhil Kaul
* Connor Passe
* Florian Wernthaler

### How to Access
Go to http://vcm-17482.vm.duke.edu:5000/. You should see the homepage, with a search bar in the center and log in and sign up options in the top right.

#### Functionalities:
Completed
* Search by ingredient(s)
* View one recipe

In progress
* Log in to/sign up for user account
* Apply additional search filters - total time, number of steps, vegetarian
* Save search filter preferences
* Save user favorites

### Tech Stack
* Flask
* SQLAlchemy
* PostgreSQL
* HTML
* CSS
* Docker

### Code Structure
The main app code is contained within app.py, with routes to the various webpages involved. HTML templates can be found within the templates folder, and CSS is in the static folder to allow access when rendering templates from the Flask app. The sql folder contains the setup SQL script and the CSV file to populate the database.
