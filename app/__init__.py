from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import create_engine, Table, ForeignKey, Column, Integer, String, Boolean
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:batman@localhost/donn"
db = SQLAlchemy(app)
db.create_all()
### BASE URL ###
BASE_URL = '/api'

### HTML STATUS CODES ###
OK = 200
UNPROCESSABLE_ENTITY = 422
NOT_FOUND = 404


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/characters")
def characters():
	return render_template("characters.html")

@app.route("/volumes")
def volumes():
	return render_template("volumes.html")

@app.route("/teams")
def teams():
	return render_template("teams.html")

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

@app.route("/character/1")
def CC():
	return render_template("chief_chirpa.html")

@app.route("/character/2")
def Sheena():
	return render_template("reef.html")

@app.route("/character/3")
def Jerry():
	return render_template("Jerry.html")

@app.route("/volume/1")
def SW():
	return render_template("star_wars.html")

@app.route("/volume/2")
def Sum():
	return render_template("summer.html")

@app.route("/volume/3")
def Jumbo():
	return render_template("planet.html")

@app.route("/team/1")
def Ewoks():
	return render_template("ewoks.html")

@app.route("/team/2")
def Mouse():
	return render_template("mouse.html")

@app.route("/team/3")
def Space():
	return render_template("space.html")


# @app.route("/character/<name>")
# def show_character(name):
# 	character = User.query.filter_by(name=name).first_or_404()
# 	return render_template("character.html", character=character)


# if __name__=="__main__":
# 	app.run()