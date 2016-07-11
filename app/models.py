# from afsiodfajf.database import Base  # afsafsf is going to be our database name
from app import db



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
    appear: first appearance
    real: real name if it exists
    num_apperances: num of appearnces
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
    appear = db.Column(db.String, unique=False)
    real = db.Column(db.String, unique=False)
    num_appearances = db.Column(db.String, unique=False)


    def __repr__(self):
        return 'Character(name={}, image={}, volumes='.format(
            self.name,
            self.image,
            self.volumes
            ) + \
            ' birth={}, gender={}, creator = {}, publisher={}, teams={}, appear={}, real={}, num_appearances={}'.format(
                self.birth,
                self.gender,
                self.creator,
                self.publisher,
                self.teams,
                self.appear,
                self.real) \
            + self.num_appearances + ")"


class Publisher(db.Model):
    """
        name: the name of the publisher
        address: address of publisher if given
        city: city of publisher
        state: state of publisher
        deck: description
        image: image url
        characters: character publisher has worked with
        volumes: volumes publisher has worked with
        teams: teams publisher has worked with
    """
    __tablename__ = "Publisher"
    name = db.Column(db.String(50), unique=True, primary_key=True)
    address = db.Column(db.String(100), unique=False)  # maybe this one?
    city = db.Column(db.String(20), unique=False)
    state = db.Column(db.String(20), unique=False)
    deck = db.Column(db.String, unique=False)
    image = db.Column(db.String)  # image url
    characters = db.relationship("Character", backref="character_publisher", lazy='dynamic')
    volumes = db.relationship("Volume", backref="volume_publisher", lazy='dynamic')
    teams = db.relationship("Team", backref="team_publisher", lazy='dynamic')

    def __repr__(self):
        return 'Publisher(name={}, address={}, city={}, state={}, deck={}, image={}, characters={}, volumes={}, teams={}'.format(
            self.name,
            self.address,
            self.city,
            self.state,
            self.deck,
            self.image,
            self.characters,
            self.volumes,
            self.teams,
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
    num_issues = db.Column(db.String)


    def __repr__(self):
        return 'Volume(image={}, description={}, count_of_issues={},  start_year={}, publisher={}, teams={}, name={}, num_issues={}'.format(
            self.image,
            self.description,
            self.count_of_issues,
            self.start_year,
            self.publisher,
            self.teams,
            self.name,
            self.num_issues
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
    appear = db.Column(db.String, unique=False)
    num_appearances = db.Column(db.String, unique=False)

    def __repr__(self):
        return 'Team(name={}, description={}, image={}, publisher={}, characters={}, volumes={}, appear={}. num_appearances={}'.format(
            self.name,
            self.description,
            self.publisher,
            self.characters,
            self.volumes,
            self.appear,
            self.num_appearances,
            ) + ")"
