from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_database import Base, Character, Publisher, Volume, Team
import random

engine = create_engine('sqlite:///komixx.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

word_file = "/usr/share/dict/words"
WORDS = open(word_file).read().splitlines()

def populateCharacters():
	for x in range(10):
		character = Character(name=unicode(random.choice(WORDS), 'utf-8'),
			birth = unicode(random.choice(WORDS), 'utf-8'),
			volumes = unicode(random.choice(WORDS), 'utf-8'),
			primary_publisher = unicode(random.choice(WORDS), 'utf-8'),
			image = unicode(random.choice(WORDS), 'utf-8'),
			volume_credits = unicode(random.choice(WORDS), 'utf-8'),
			powers = unicode(random.choice(WORDS), 'utf-8'),
			gender = unicode(random.choice(WORDS), 'utf-8'),
			creator =  unicode(random.choice(WORDS), 'utf-8'))
		session.add(character)
		session.commit()

def populatePublishers():
	for x in range(10):
		publisher = Publisher(name=unicode(random.choice(WORDS), 'utf-8'),
			characters = unicode(random.choice(WORDS), 'utf-8'),
			locAd = unicode(random.choice(WORDS), 'utf-8'),
			city = unicode(random.choice(WORDS), 'utf-8'),
			state = unicode(random.choice(WORDS), 'utf-8'),
			deck = unicode(random.choice(WORDS), 'utf-8'),
			image = unicode(random.choice(WORDS), 'utf-8'),
			volumes = unicode(random.choice(WORDS), 'utf-8'),
			teams =  unicode(random.choice(WORDS), 'utf-8'))
		session.add(publisher)
		session.commit()

def populateVolumes():
	for x in range(10):
		volume = Volume(image=unicode(random.choice(WORDS), 'utf-8'),
			description = unicode(random.choice(WORDS), 'utf-8'),
			publisher = unicode(random.choice(WORDS), 'utf-8'),
			count_of_issues = 5,
			characters = unicode(random.choice(WORDS), 'utf-8'),
			aliases = unicode(random.choice(WORDS), 'utf-8'),
			start_year = 2016)
		session.add(volume)
		session.commit()

def populateTeams():
	for x in range(10):
		team = Team(name=unicode(random.choice(WORDS), 'utf-8'),
			publisher = unicode(random.choice(WORDS), 'utf-8'),
			description = unicode(random.choice(WORDS), 'utf-8'),
			image = unicode(random.choice(WORDS), 'utf-8'),
			aliases = unicode(random.choice(WORDS), 'utf-8'),
			volume_credits = unicode(random.choice(WORDS), 'utf-8'),
			characters = unicode(random.choice(WORDS), 'utf-8'),
			team_members = unicode(random.choice(WORDS), 'utf-8'),
			character_enemies = unicode(random.choice(WORDS), 'utf-8'),
			character_allies = unicode(random.choice(WORDS), 'utf-8'))
		session.add(team)
		session.commit()

populateCharacters()
populatePublishers()
populateVolumes()
populateTeams()

print("done.")

