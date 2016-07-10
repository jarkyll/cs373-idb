from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_database import Base, Character, Publisher, Volume, Team

engine = create_engine('sqlite:///komixx.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/hello')
def HelloWorld():
	c = session.query(Character).first()
	print(c)
	return '' + c.name


if __name__== "__main__":
	app.run()
