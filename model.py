from sqlalchemy import Column, Integer, String
from afsiodfajf.database import Base # afsafsf is going to be our database name

#db.Model is the base class for all of our models
class Character(db.Model):
    __tablename__ = "Characters"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), unique=True)
    birthplace = db.Column(String(100), unique=False)
    volumes = db.Column(db.PickleType(mutable=True)) # maybe this one?
    publisher = db.Column(String(30), unique=False)
    image = db.Column(String)# image url

class Publisher(db.Model):
    __tablename__ = "Publisher"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), unique=True)
    characters = db.Column(db.PickleType(mutable=True))
    locAd = db.Column(String(100), unique=false) # maybe this one?
    city = db.Column(String(20), unique=False)
    state = db.Column(String(2), unique=False)
    description = db.Column(String, unique=False)

class Volume(db.Model):
    __tablename__ = "Volume"
    id = db.Column(Integer, primary_key=True)
    image = db.Column(String)# image url
    description = db.Column(String(200), unique=False)
    publisher = db.Column(String, unique=False)
    count = db.Column(Integer, unique=false)
    characters = db.Column(db.PickleType(mutable=True))

class Series(db.Model):
    __tablename__ = "Series"
    id = db.Column(Integer, primary_key=True)
    publisher = db.Column(String(50), unique=False)
    description = db.Column(String, unique=False)
    image = db.Column(String)# image url
    start_year = db.Column(Integer, unique=False)
    characters = db.Column(db.PickleType(mutable=True))`