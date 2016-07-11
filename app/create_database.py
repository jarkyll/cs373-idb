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

	@property 
	def serialize(self):
		return {
			'name': self.name,
			'birth' : self.birth,
			'volumes' : self.volumes,
			'primary_publisher' : self.primary_publisher,
			'image' : self.image,
			'volume_credits' : self.volume_credits,
			'powers' : self.powers,
			'gender' : self.gender,
			'creator' : self.creator
		} 


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

	@property 
	def serialize(self):
		return {
			'name': self.name,
			'characters' : self.characters,
			'locAd' : self.locAd,
			'city' : self.city,
			'state' : self.state,
			'deck' : self.deck,
			'image' : self.image,
			'volumes' : self.volumes,
			'teams' : self.teams
		} 


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

	@property 
	def serialize(self):
		return {
			'image': self.image,
			'description' : self.description,
			'publisher' : self.publisher,
			'count_of_issues' : self.count_of_issues,
			'characters' : self.characters,
			'aliases' : self.aliases,
			'start_year' : self.start_year
		} 


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

	@property 
	def serialize(self):
		return {
			'name': self.name,
			'publisher' : self.publisher,
			'description' : self.description,
			'image' : self.image,
			'aliases' : self.aliases,
			'volume_credits' : self.volume_credits,
			'characters' : self.characters,
			'team_members' : self.team_members,
			'character_enemies' : self.character_enemies,
			'character_allies' : self.character_allies
		} 


engine = create_engine('sqlite:///komixx.db')
Base.metadata.create_all(engine)