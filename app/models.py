from sqlalchemy import Table, ForeignKey, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


BASE = declarative_base()
# from afsiodfajf.database import Base  # afsafsf is going to be our database name

# main is the base class for all of our models
# whatever
characters_volumes = Table('characters_volumes', BASE.metadata,
    Column('volume_name', String(100), ForeignKey('Volume.name')),
    Column('character_name', String(150), ForeignKey('Character.name'))
)

characters_teams = Table('characters_teams', BASE.metadata,
    Column('character_name', String(200), ForeignKey('Character.name')),
    Column('team_name', String(250), ForeignKey('Team.name'))
)

volumes_teams = Table('volumes_teams', BASE.metadata,
    Column('volume_name', String(200), ForeignKey('Volume.name')),
    Column('team_name', String(150), ForeignKey('Team.name'))
)


class Character(BASE):
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
    name = Column(String(150), unique=True, primary_key=True)
    birth = Column(String(100), unique=False)
    image = Column(String)  # image url
    gender = Column(String(10))
    creator = Column(String(50), unique=False)
    volumes = relationship("Volume", secondary=characters_volumes, back_populates="characters")
    teams = relationship("Team", secondary=characters_teams, back_populates="characters")
    publisher = relationship("Publisher",  back_populates="characters")

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


class Publisher(BASE):
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
    name = Column(String(50), unique=True, primary_key=True)
    address = Column(String(100), unique=False)  # maybe this one?
    city = Column(String(20), unique=False)
    state = Column(String(2), unique=False)
    deck = Column(String, unique=False)
    image = Column(String)  # image url
    characters = relationship("Character", back_populates="publisher")
    volumes = relationship("Volume", back_populates="publisher")
    teams = relationship("Team", back_populates="publisher")

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


class Volume(BASE):
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
    image = Column(String)  # image url
    description = Column(String(200), unique=False)
    count_of_issues = Column(Integer, unique=False)
    start_year = Column(Integer, unique=False)
    publisher = relationship("Publisher",  back_populates="volumes")
    characters = relationship("Volume", secondary=characters_volumes, back_populates="volumes")
    teams = relationship("Team", secondary=volumes_teams, back_populates="volumes")
    name = Column(String, unique=True, primary_key=True)
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


class Team(BASE):
    """
        name: name of team
        description: description of team
        image: image url
        publisher: main publisher for team
        characters: characters in team
        volumes: volumes that team appeard in
    """
    __tablename__ = "Team"
    name = Column(String(50), unique=True, primary_key=True)
    description = Column(String, unique=False)
    image = Column(String)  # image url
    publisher = relationship("Publisher", back_populates="teams")
    characters = relationship("Character",  back_populates="teams")
    volumes = relationship("Volume", secondary=volumes_teams, back_populates="teams")


    def __repr__(self):
        return 'Team(name={}, description={}, image={}, publisher={}, characters={}, volumes={}'.format(
            self.name,
            self.description,
            self.publisher,
            self.characters,
            self.volumes,
            ) + ")"
