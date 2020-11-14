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
* Search by one or multiple ingredients
* View one recipe
* Log in to/sign up for user account
* Apply additional search filters - total time, number of steps, vegetarian

### Tech Stack
* Flask
* SQLAlchemy
* PostgreSQL
* HTML
* CSS
* Docker

### Code Structure
The main app code is contained within app.py, with routes to the various webpages involved. HTML templates can be found within the templates folder, and CSS is in the static folder to allow access when rendering templates from the Flask app. The sql folder contains the setup SQL script and the CSV file to populate the database.

### Resources
Main page background image: https://pixabay.com/images/id-1898194/
