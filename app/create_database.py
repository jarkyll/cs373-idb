import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Character(Base):
	__tablename__ = 'character'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	birth = Column(String(250), nullable=False)
	volumes = Column(String(250), nullable=False)
	primary_publisher = Column(String(250), nullable=False)
	image = Column(String(250), nullable=False)
	volume_credits = Column(String(250), nullable=False)
	powers = Column(String(250), nullable=False)
	gender = Column(String(250), nullable=False)
	creator = Column(String(250), nullable=False)  

class Publisher(Base):
	__tablename__ = 'publisher'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	characters = Column(String(250), nullable=False)
	locAd = Column(String(250), nullable=False)
	city = Column(String(250), nullable=False)
	state = Column(String(250), nullable=False)
	deck = Column(String(250), nullable=False)
	image = Column(String(250), nullable=False)
	volumes = Column(String(250), nullable=False)
	teams = Column(String(250), nullable=False)

class Volume(Base):
	__tablename__ = 'volume'
	id = Column(String(250), primary_key=True)
	image = Column(String(250), nullable=False)
	description = Column(String(250), nullable=False)
	publisher = Column(String(250), nullable=False)
	count_of_issues = Column(Integer, nullable=False)
	characters = Column(String(250), nullable=False)
	aliases = Column(String(250), nullable=False)
	start_year = Column(Integer, nullable=False)

class Team(Base):
	__tablename__ = 'team'
	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable=False)
	publisher = Column(String(250), nullable=False)
	description = Column(String(250), nullable=False)
	image = Column(String(250), nullable=False)
	aliases = Column(String(250), nullable=False)
	volume_credits = Column(String(250), nullable=False)
	characters = Column(String(250), nullable=False)
	team_members = Column(String(250), nullable=False)
	character_enemies = Column(String(250), nullable=False)
	character_allies = Column(String(250), nullable=False)	

engine = create_engine('sqlite:///komixx.db')
Base.metadata.create_all(engine)