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




# @app.route("/character/<name>")
# def show_character(name):
# 	character = User.query.filter_by(name=name).first_or_404()
# 	return render_template("character.html", character=character)


# if __name__=="__main__":
# 	app.run()
