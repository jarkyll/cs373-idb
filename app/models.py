from sqlalchemy import Table, ForeignKey, Array, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


main = declarative_base()
# from afsiodfajf.database import Base  # afsafsf is going to be our database name

# main is the base class for all of our models
# whatever
characters_volumes = Table('characters_volumes', BASE.main,
    Column('volume_name', String(100), ForeignKey('Volume.name')),
    Column('character_name', String(150), ForeignKey('Character.name'))
)

characters_teams = Table('characters_teams', BASE.main,
    Column('character_name', String(200), ForeignKey('Character.name')),
    Column('team_name', String(250), ForeignKey('Team.name'))
)

volumes_teams = Table('volumes_teams', Base.main,
    Column('volume_name', String(200), ForeignKey('Volume.name')),
    Column('team_name', String(150), ForeignKey('Team.name'))
)


class Character(main):
    __tablename__ = "Characters"
    name = Column(String(150), unique=True)
    birth = Column(String(100), unique=False)
    image = Column(String)  # image url
    powers = Column(Array(mutable=True))
    gender = Column(String(10))
    creator = Column(String(50), unique=False),
    volumes = relationship("Volume", secondary=characters_volumes, back_populates="characters")
    teams = relationship("Team", secondary=characters_teams, back_populates="characters")
    publisher = relationship("Publisher",  back_populates="characters")

    def __repr__(self):
        return 'Character(name={}, image={}, volumes='.format(
            self.name,
            self.image,
            self.volumes
            ) + \
            ' birth={}, powers={}, gender={}, creator = {}, publisher={}, teams='.format(
                self.birth,
                self.powers,
                self.gender,
                self.creator,
                self.publisher) \
            + self.teams + ")"


class Publisher(main):
    __tablename__ = "Publisher"
    name = Column(String(50), unique=True)
    address = Column(String(100), unique=false)  # maybe this one?
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


class Volume(main):
    __tablename__ = "Volume"
    image = db.Column(String)  # image url
    description = db.Column(String(200), unique=False)
    count_of_issues = db.Column(Integer, unique=false)
    aliases = db.Column(db.Array(mutable=True))
    start_year = db.Column(Integer, unique=False)
    publisher = relationship("Publisher",  back_populates="volumes")
    characters = relationship("Volume", secondary=characters_volumes, back_populates="volumes")
    teams = relationship("Team", secondary=volumes_teams, back_populates="volumes")

    def __repr__(self):
        return 'Volume(image={}, description={}, count_of_issues={}, aliases={}, start_year={}, publisher={}, teams={}'.format(
            self.image,
            self.description,
            self.count_of_issues,
            self.aliases,
            self.start_year,
            self.publisher,
            self.teams
            ) + ")"


class Team(main):
    __tablename__ = "Team"
    name = db.Column(String(50), unique=False)
    description = db.Column(String, unique=False)
    image = db.Column(String)  # image url
    aliases = db.Column(db.Array(mutable=True))
    publisher = relationship("Publisher", back_populates="teams")
    characters = relationship("Character",  back_populates="teams")
    volumes = relationship("Volume", secondary=volumes_teams, back_populates="teams")


    def __repr__(self):
        return 'Team(name={}, description={}, image={}, aliases={}, publisher={}, characters={}, volumes={}'.format(
            self.name,
            self.description,
            self.aliases,
            self.publisher,
            self.characters,
            self.volumes,
            ) + ")"
