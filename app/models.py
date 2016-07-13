# from afsiodfajf.database import Base  # afsafsf is going to be our database name
from manage import db

CHARACTERS_VOLUMES = db.Table('characters_volumes',
                              db.Column('character_name', db.String(150), db.ForeignKey('Character.name')),
                              db.Column('volume_name', db.String(100), db.ForeignKey('Volume.name')))

CHARACTER_TEAMS = db.Table('characters_teams',
                            db.Column('character_name', db.String(200), db.ForeignKey('Character.name')),
                            db.Column('team_name', db.String(250), db.ForeignKey('Team.name')))

VOLUME_TEAMS = db.Table('volumes_teams',
                         db.Column('volume_name', db.String(200), db.ForeignKey('Volume.name')),
                         db.Column('team_name', db.String(150), db.ForeignKey('Team.name')))


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

    appear = db.Column(db.String, unique=False)
    real = db.Column(db.String, unique=False)
    num_appearances = db.Column(db.String, unique=False)

    publisher_name = db.Column(db.String(150), db.ForeignKey('Publisher.name'))
    character_publisher = db.relationship("Publisher", back_populates="publisher_characters")

    character_volumes = db.relationship("Volume", secondary=characters_volumes, back_populates="volume_characters")

    character_teams = db.relationship("Team", secondary=characters_teams, back_populates="team_characters")

    def json_it(self):
        t = []
        for team in self.character_teams:
            t += {'name': team.name, 'image': team.image}
        v = []
        for volume in self.character_volumes:
            v += {'name': volume.name, 'image': volume.image}

        ans = {
            'name': self.name,
            'appear': self.appear,
            'birth': self.birth,
            'character_publisher': self.character_publisher,
            'creator': self.creator,
            'gender': self.gender,
            'image': self.image,
            'num_appearances': self.num_appearances,
            'real': self.real,
            'character_teams': t,
            'character_volumes': v
        }
        return ans

    def __repr__(self):
        return 'Character(name={}, image={}, birth={}, gender={}, creator={}, publisher={}, appear={}, real={}, num_appearances={}'.format(
            self.name,
            self.image,
            self.birth,
            self.gender,
            self.creator,
            self.publisher_name,
            self.appear,
            self.real,
            self.num_appearances
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
    start_year = db.Column(db.Integer, unique=False)
    name = db.Column(db.String, unique=True, primary_key=True)
    num_issues = db.Column(db.String)

    publisher_name = db.Column(db.String(150), db.ForeignKey('Publisher.name'))
    volume_publisher = db.relationship("Publisher", back_populates="publisher_volumes")

    volume_characters = db.relationship("Character", secondary='characters_volumes', back_populates="character_volumes")

    volume_teams = db.relationship("Team", secondary=volumes_teams, back_populates='team_volumes')

    def json_it(self):
        t = []
        for team in self.volume_teams:
            temp = {'name': team.name, 'image': team.image}
            t.append(temp)
        c = []
        for character in self.volume_characters:
            temp = {'name': character.name, 'image': character.image}
            c.append(temp)

        ans = {
            'description': self.description,
            'image': self.image,
            'name': self.name,
            'num_issues': self.num_issues,
            'publisher_name': self.publisher_name,
            'start_year': self.start_year,
            'volume_teams': t,
            'volume_characters': c
        }
        return ans

    def __repr__(self):
        return 'Volume(image={}, description={}, start_year={}, publisher={}, name={}, num_issues={}'.format(
            self.image,
            self.description,
            self.start_year,
            self.publisher_name,
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
    appear = db.Column(db.String, unique=False)
    num_appearances = db.Column(db.String, unique=False)

    publisher_name = db.Column(db.String(150), db.ForeignKey('Publisher.name'))
    team_publisher = db.relationship("Publisher", back_populates="publisher_teams")

    team_characters = db.relationship("Character", secondary=characters_teams, back_populates='character_teams')
    team_volumes = db.relationship("Volume", secondary=volumes_teams, back_populates='volume_teams')

    def __repr__(self):
        return 'Team(name={}, description={}, image={}, publisher={}, appear={}, num_appearances={}'.format(
            self.name,
            self.description,
            self.image,
            self.team_publisher,
            self.appear,
            self.num_appearances,
        ) + ")"

    def json_it(self):
        c = []
        for char in self.team_characters:
            temp = {'name': char.name, 'image': char.image}
            c.append(temp)
        v = []
        for volume in self.team_volumes:
            temp = {'name': volume.name, 'image': volume.image}
            v.append(temp)
        ans = {
            'appear': self.appear,
            'description': self.description,
            'image': self.image,
            'name': self.name,
            'num_appearances': self.num_appearances,
            'publisher_name': self.publisher_name,
            'image': self.image,
            'num_appearances': self.num_appearances,
            'team_characters': c,
            'team_volumes': v
        }
        return ans


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

    publisher_characters = db.relationship("Character", back_populates="character_publisher")

    publisher_volumes = db.relationship("Volume", back_populates="volume_publisher")

    publisher_teams = db.relationship("Team", back_populates="team_publisher")

    def __repr__(self):
        return 'Publisher(name={}, address={}, city={}, state={}, deck={}, image={}, publisher_characters={},publisher_volumes={}, publisher_teams={}'.format(
            self.name,
            self.address,
            self.city,
            self.state,
            self.deck,
            self.image,
            self.publisher_characters,
            self.publisher_volumes,
            self.publisher_teams,
        ) + ")"

    def json_it(self):
        list_t = []
        for team in self.publisher_teams:
            temp = {'name': team.name, 'image': team.image}
            list_t.append(temp)
        list_vol = []
        for volume in self.publisher_volumes:
            temp = {'name': volume.name, 'image': volume.image}
            list_vol.append(temp)
        list_char = []
        for character in self.publisher_characters:
            temp = {'name': character.name, 'image': character.image}
            list_char.append(temp)
        ans = {
            'name': self.name,
            'city': self.city,
            'deck': self.deck,
            'address': self.address,
            'image': self.image,
            'state': self.state,
            'publisher_characters': list_char,
            'publisher_teams': list_t,
            'publisher_volumes': list_vol
        }
        return ans
