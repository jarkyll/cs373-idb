from flask import Flask, render_template, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_database import Base, Character, Publisher, Volume, Team

engine = create_engine('sqlite:///komixx.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

### Pages


@app.route('/hello')
def HelloWorld():
	return 'home'

@app.route("/home")
def homepage():
	return render_template("index.html")

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/characters')
def characters():
	return render_template('characters.html')

@app.route('/volumes')
def volumes():
	return render_template('volumes.html')

@app.route('/teams')
def teams():
	return render_template('teams.html')

@app.route('/publishers')
def publishers():
	return render_template('publishers.html')

### API
@app.route('/api/characters')
def character_api():
	characters = session.query(Character).all()
	return jsonify(Character=[c.serialize for c in characters])

@app.route('/api/publishers')
def publisher_api():
	publishers = session.query(Publisher).all()
	return jsonify(Publisher=[p.serialize for p in publishers])

@app.route('/api/volumes')
def volume_api():
	volumes = session.query(Volume).all()
	return jsonify(Volume=[v.serialize for v in volumes])

@app.route('/api/teams')
def team_api():
	teams = session.query(Team).all()
	return jsonify(Team=[t.serialize for t in teams])


if __name__== "__main__":
	app.run()
