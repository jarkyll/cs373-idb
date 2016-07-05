from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from SQLAlchemy import Column, Integer, String
from afsiodfajf.database import Base  # afsafsf is going to be our database name

# db.Model is the base class for all of our models
# whatever

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 
# db = sqlalchemy(app)


class Character(db.Model):
    __tablename__ = "Characters"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), unique=True)
    birth = db.Column(String(100), unique=False)
    volumes = db.Column(db.Array(mutable=True))  # maybe this one?
    primary_publisher = db.Column(String(30), unique=False)
    image = db.Column(String)  # image url
    volume_credits = db.Column(db.Array(mutable=True))
    powers = db.Column(db.Array(mutable=True))
    gender = db.Column(String(10))
    creator = db.Column(String(50), unique=False)


class Publisher(db.Model):
    __tablename__ = "Publisher"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), unique=True)
    characters = db.Column(db.Array(mutable=True))
    locAd = db.Column(String(100), unique=false)  # maybe this one?
    city = db.Column(String(20), unique=False)
    state = db.Column(String(2), unique=False)
    deck = db.Column(String, unique=False)
    image = db.Column(String)  # image url
    volumes = db.Column(db.Array(mutable=True))
    teams = db.Column(db.Array(mutable=True))


class Volume(db.Model):
    __tablename__ = "Volume"
    id = db.Column(Integer, primary_key=True)
    image = db.Column(String)  # image url
    description = db.Column(String(200), unique=False)
    publisher = db.Column(String, unique=False)
    count_of_issues = db.Column(Integer, unique=false)
    characters = db.Column(db.Array(mutable=True))
    aliases = db.Column(db.Array(mutable=True))
    start_year = db.Column(Integer, unique=False)


class Team(db.Model):
    __tablename__ = "Team"
    name = db.Column(String(50), unique=False)
    id = db.Column(Integer, primary_key=True)
    publisher = db.Column(String(50), unique=False)
    description = db.Column(String, unique=False)
    image = db.Column(String)  # image url
    aliases = db.Column(db.Array(mutable=True))
    volume_credits = db.Column(db.Array(mutable=True))
    characters = db.Column(db.Array(mutable=True))
    team_members = db.Column(db.Array(mutable=True))
    character_enemies = db.Column(db.Array(mutable=True))
    character_allies = db.Column(db.Array(mutable=True))
