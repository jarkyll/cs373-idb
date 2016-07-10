import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Character(Base):
	__tablename__ = 'character'
	id = Column(Integer, primary_key=True)
	name = Column(UnicodeText(64), nullable=False)
	birth = Column(UnicodeText(64), nullable=False)
	volumes = Column(UnicodeText(64), nullable=False)
	primary_publisher = Column(UnicodeText(64), nullable=False)
	image = Column(UnicodeText(64), nullable=False)
	volume_credits = Column(UnicodeText(64), nullable=False)
	powers = Column(UnicodeText(64), nullable=False)
	gender = Column(UnicodeText(64), nullable=False)
	creator = Column(UnicodeText(64), nullable=False)  

class Publisher(Base):
	__tablename__ = 'publisher'
	id = Column(Integer, primary_key=True)
	name = Column(UnicodeText(64), nullable=False)
	characters = Column(UnicodeText(64), nullable=False)
	locAd = Column(UnicodeText(64), nullable=False)
	city = Column(UnicodeText(64), nullable=False)
	state = Column(UnicodeText(64), nullable=False)
	deck = Column(UnicodeText(64), nullable=False)
	image = Column(UnicodeText(64), nullable=False)
	volumes = Column(UnicodeText(64), nullable=False)
	teams = Column(UnicodeText(64), nullable=False)

class Volume(Base):
	__tablename__ = 'volume'
	id = Column(Integer, primary_key=True)
	image = Column(UnicodeText(64), nullable=False)
	description = Column(UnicodeText(64), nullable=False)
	publisher = Column(UnicodeText(64), nullable=False)
	count_of_issues = Column(Integer, nullable=False)
	characters = Column(UnicodeText(64), nullable=False)
	aliases = Column(UnicodeText(64), nullable=False)
	start_year = Column(Integer, nullable=False)

class Team(Base):
	__tablename__ = 'team'
	id = Column(Integer, primary_key = True)
	name = Column(UnicodeText(64), nullable=False)
	publisher = Column(UnicodeText(64), nullable=False)
	description = Column(UnicodeText(64), nullable=False)
	image = Column(UnicodeText(64), nullable=False)
	aliases = Column(UnicodeText(64), nullable=False)
	volume_credits = Column(UnicodeText(64), nullable=False)
	characters = Column(UnicodeText(64), nullable=False)
	team_members = Column(UnicodeText(64), nullable=False)
	character_enemies = Column(UnicodeText(64), nullable=False)
	character_allies = Column(UnicodeText(64), nullable=False)	

engine = create_engine('sqlite:///komixx.db')
Base.metadata.create_all(engine)