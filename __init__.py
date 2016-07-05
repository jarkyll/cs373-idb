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
	return "this html is about the list of characters"


@app.route("/comicseries")
def series():
	return "this html is about the list of comic book series"

@app.route("/publishers")
def publishers():
	return "this html is about the list of comic book publishers"



if __name__=="__main__":
	app.run()
