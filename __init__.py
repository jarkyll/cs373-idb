from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


app = Flask(__name__)
db.init_app(app)

@app.route("/")
def homepage():
	return render_template("index.html")


@app.route("/about")
def about():
	return "this html is about us"


@app.route("/characters")
def characters():
	return render_template("character_template.html")

@app.route("/volumes")
def volumes():
	return render_template("volumes_template.html")

@app.route("/teams")
def teams():
	return render_template("teams_template.html")

@app.route("/team/1")
def team_1():
	return render_template("team_1.html")


@app.route("/publishers")
def publishers():
	return render_template("publishers.html")


@app.route("/publisher/1")
def DH():
	return render_template("publisher_dark_horse.html")

@app.route("/publisher/2")
def FH():
	return render_template("publisher_fiction_house.html")

@app.route("/publisher/3")
def Dell():
	return render_template("publisher_dell.html")


if __name__=="__main__":
	app.run()
