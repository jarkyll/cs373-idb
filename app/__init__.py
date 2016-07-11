from flask import Flask, render_template
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import create_engine, Table, ForeignKey, Column, Integer, String, Boolean
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:batman@localhost/don"
db = SQLAlchemy(app)



characters_volumes = db.Table('characters_volumes',
    db.Column('character_name', db.String(150), db.ForeignKey('Character.name')),
    db.Column('volume_name', db.String(100), db.ForeignKey('Volume.name'))
)


characters_teams = db.Table('characters_teams',
    db.Column('character_name', db.String(200), db.ForeignKey('Character.name')),
    db.Column('team_name', db.String(250), db.ForeignKey('Team.name'))
)

volumes_teams = db.Table('volumes_teams',
    db.Column('volume_name', db.String(200), db.ForeignKey('Volume.name')),
    db.Column('team_name', db.String(150), db.ForeignKey('Team.name'))
)


class Character(db.Model):
    """
    name: name of characters
    birth: when the character was born
    image: image url
    gender: male or female
    creator: creator name
    volumes: volumes that character is in
    teams: teams that character is in
    publisher: publisher character is with
    """
    __tablename__ = "Character"
    name = db.Column(db.String(150), unique=True, primary_key=True)
    birth = db.Column(db.String(100), unique=False)
    image = db.Column(db.String)  # image url
    gender = db.Column(db.String(10))
    creator = db.Column(db.String(50), unique=False)
    publisher = db.Column(db.String(150), db.ForeignKey('Publisher.name'))
    volumes = db.relationship("Volume", secondary=characters_volumes, backref=db.backref("volumes_character", lazy='dynamic'))
    teams = db.relationship("Team", secondary=characters_teams, backref=db.backref("teams_character", lazy='dynamic'))



    def __repr__(self):
        return 'Character(name={}, image={}, volumes='.format(
            self.name,
            self.image,
            self.volumes
            ) + \
            ' birth={}, gender={}, creator = {}, publisher={}, teams='.format(
                self.birth,
                self.gender,
                self.creator,
                self.publisher) \
            + self.teams + ")"


class Publisher(db.Model):
    """
        name: the name of the publisher
        address: address of publisher if given
        city: city of publisher
        state: state of publisher
        deck: description
        image: image url
        characters: character publisher has worked with
        volumes: volumes character has worked with
    """
    __tablename__ = "Publisher"
    name = db.Column(db.String(50), unique=True, primary_key=True)
    address = db.Column(db.String(100), unique=False)  # maybe this one?
    city = db.Column(db.String(20), unique=False)
    state = db.Column(db.String(2), unique=False)
    deck = db.Column(db.String, unique=False)
    image = db.Column(db.String)  # image url
    characters = db.relationship("Character", backref="character_publisher", lazy='dynamic')
    volumes = db.relationship("Volume", backref="volume_publisher", lazy='dynamic')
    teams = db.relationship("Team", backref="team_publisher", lazy='dynamic')

    def __repr__(self):
        return 'Publisher(name={}, address={}, city={}, state={}, deck={}, volumes={}, teams={}'.format(
            self.name,
            self.address,
            self.city,
            self.state,
            self.deck,
            self.volumes,
            self.teams
            ) + ")"


class Volume(db.Model):
    """
    image: image url
    description: info on volume
    count_of_issues: num issues in volume
    start_year: when volume started
    publisher: main publisher
    characters: characters in volume
    teams: teams in the characters
    name: name of volume
    """
    __tablename__ = "Volume"
    image = db.Column(db.String)  # image url
    description = db.Column(db.String(200), unique=False)
    count_of_issues = db.Column(db.Integer, unique=False)
    start_year = db.Column(db.Integer, unique=False)
    publisher = db.Column(db.String(150), db.ForeignKey('Publisher.name'))
    characters = db.relationship("Volume", secondary=characters_volumes, backref=db.backref("characters_volume", lazy='dynamic'))
    teams = db.relationship("Team", secondary=volumes_teams, backref=db.backref('teams_volume', lazy='dynamic'))
    name = db.Column(db.String, unique=True, primary_key=True)
    def __repr__(self):
        return 'Volume(image={}, description={}, count_of_issues={},  start_year={}, publisher={}, teams={}'.format(
            self.image,
            self.description,
            self.count_of_issues,
            self.start_year,
            self.publisher,
            self.teams,
            self.name
            ) + ")"


class Team(db.Model):
    """
        name: name of team
        description: description of team
        image: image url
        publisher: main publisher for team
        characters: characters in team
        volumes: volumes that team appeard in
    """
    __tablename__ = "Team"
    name = db.Column(db.String(50), unique=True, primary_key=True)
    description = db.Column(db.String, unique=False)
    image = db.Column(db.String)  # image url
    publisher = db.Column(db.String(150), db.ForeignKey('Publisher.name'))
    characters = db.relationship("Character", secondary=characters_teams, backref=db.backref('character_teams', lazy='dynamic'))
    volumes = db.relationship("Volume", secondary=volumes_teams, backref=db.backref('volume_teams', lazy='dynamic'))


    def __repr__(self):
        return 'Team(name={}, description={}, image={}, publisher={}, characters={}, volumes={}'.format(
            self.name,
            self.description,
            self.publisher,
            self.characters,
            self.volumes,
            ) + ")"

db.create_all()

### BASE URL ###
BASE_URL = '/api'

### HTML STATUS CODES ###
OK = 200
UNPROCESSABLE_ENTITY = 422
NOT_FOUND = 404


DEMO = {
	'name': "tesing"
}

pub = Volume(**DEMO)

try:
	db.session.add(pub)
	db.session.commit()
except:
	db.session.rollback()
	raise
finally:
	db.session.close()


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

@app.route("/character/<name>")
def show_character(name):
	character = User.query.filter_by(name=name).first_or_404()
	return render_template("character.html", character=character)




if __name__=="__main__":
	app.run()
