from flask import Flask, render_template, jsonify, abort
import subprocess
import jinja2
import unittest, sys
import json
import urllib
import pprint
import glob, os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy import and_, or_
from sqlalchemy.engine.url import URL
from sqlalchemy.types import UserDefinedType
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:batman@localhost/donn"
db = SQLAlchemy(app)
db.create_all()




class TsVector(UserDefinedType):
    """Holds a TsVector column which is the data type needed
        for the texxt search"""

    name = "TSVECTOR"

    def get_col_spec(self):
        ''' we just return tsvector
        '''
        return self.name

PublisherName = ['Vertigo', 'IDW Publishing', 'Dark Horse Comics', 'Top Cow', 'Valiant', 'Dell', 'Aftershock Comics',
                 'Image', 'Fiction House', 'Boom! Studios']
dir = os.getcwd() + '/'


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

    appear = db.Column(db.String, unique=False)
    real = db.Column(db.String, unique=False)
    num_appearances = db.Column(db.String, unique=False)

    publisher_name = db.Column(db.String(150), db.ForeignKey('Publisher.name'))
    character_publisher = db.relationship("Publisher", back_populates="publisher_characters")

    character_volumes = db.relationship("Volume", secondary=characters_volumes, back_populates="volume_characters")

    character_teams = db.relationship("Team", secondary=characters_teams, back_populates="team_characters")


     # TsVector column used for searching.
    tsvector_col = db.Column(TsVector)

    # Create an index for the tsvector column
    __table_args__ = (
        db.Index('character_tsvector_idx', 'tsvector_col', postgresql_using='gin'),)

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


# Trigger that updates Characters and their triggers
CHARACTER_VECTOR_TRIGGER = db.DDL("""
    CREATE TRIGGER character_tsvector_update BEFORE INSERT OR UPDATE ON "Character" FOR EACH ROW EXECUTE PROCEDURE
    tsvector_update_trigger(tsvector_col, 'pg_catalog.english', 'name', 'publisher_name', 'appear' )
    """)
db.event.listen(Character.__table__, 'after_create',
             CHARACTER_VECTOR_TRIGGER.execute_if(dialect='postgresql'))


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
    start_year = db.Column(db.String(100), unique=False)
    name = db.Column(db.String, unique=True, primary_key=True)
    num_issues = db.Column(db.String)

    publisher_name = db.Column(db.String(150), db.ForeignKey('Publisher.name'))
    volume_publisher = db.relationship("Publisher", back_populates="publisher_volumes")

    volume_characters = db.relationship("Character", secondary='characters_volumes', back_populates="character_volumes")

    volume_teams = db.relationship("Team", secondary=volumes_teams, back_populates='team_volumes')

    # TsVector column used for searching.
    tsvector_col = db.Column(TsVector)

    # Create an index for the tsvector column
    __table_args__ = (
        db.Index('volume_tsvector_idx', 'tsvector_col', postgresql_using='gin'),)

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

# Trigger that updates Volumes and their triggers
VOLUME_VECTOR_TRIGGER = db.DDL("""
    CREATE TRIGGER volume_tsvector_update BEFORE INSERT OR UPDATE ON "Volume" FOR EACH ROW EXECUTE PROCEDURE
    tsvector_update_trigger(tsvector_col, 'pg_catalog.english', 'name', 'start_year', 'publisher_name' )
    """)
db.event.listen(Volume.__table__, 'after_create',
             VOLUME_VECTOR_TRIGGER.execute_if(dialect='postgresql'))

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

    # TsVector column used for searching.
    tsvector_col = db.Column(TsVector)

    # Create an index for the tsvector column
    __table_args__ = (
        db.Index('team_tsvector_idx', 'tsvector_col', postgresql_using='gin'),)

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
# Trigger that updates Teams and their triggers
TEAM_VECTOR_TRIGGER = db.DDL("""
    CREATE TRIGGER team_tsvector_update BEFORE INSERT OR UPDATE ON "Team" FOR EACH ROW EXECUTE PROCEDURE
    tsvector_update_trigger(tsvector_col, 'pg_catalog.english', 'name', 'publisher_name', 'appear')
    """)
db.event.listen(Team.__table__, 'after_create',
             TEAM_VECTOR_TRIGGER.execute_if(dialect='postgresql'))

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


    # TsVector column used for searching.
    tsvector_col = db.Column(TsVector)

    # Create an index for the tsvector column
    __table_args__ = (
        db.Index('publishers_tsvector_idx', 'tsvector_col', postgresql_using='gin'),)

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


# Trigger that updates Teams and their triggers
PUBLISHER_VECTOR_TRIGGER = db.DDL("""
    CREATE TRIGGER publisher_tsvector_update BEFORE INSERT OR UPDATE ON "Publisher" FOR EACH ROW EXECUTE PROCEDURE
    tsvector_update_trigger(tsvector_col, 'pg_catalog.english', 'name', 'city', 'state', 'address')
    """)
db.event.listen(Publisher.__table__, 'after_create',
             PUBLISHER_VECTOR_TRIGGER.execute_if(dialect='postgresql'))




@app.route("/")
def homepage():
    return render_template("index.html")

@app.route('/runtests', methods=['GET'])
def runtests():
    try:
        result = subprocess.check_output("python3 tests.py", stderr=subprocess.STDOUT, shell=True)
        return result
    except Exception as e:
        return str(e)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/characters")
def characters():
    character = db.session.query(Character).all()
    return render_template('characters.html', characters=character)


@app.route("/volumes")
def volumes():
    volume = db.session.query(Volume).all()
    return render_template("volumes.html", volumes=volume)


@app.route("/teams")
def teams():
    team = db.session.query(Team).all()
    return render_template("teams.html", teams=team)


@app.route("/publishers")
def publishers():
    publisher = db.session.query(Publisher).all()
    return render_template("publishers.html", publishers=publisher)


@app.route("/publisher/<name>")
def publisher(name):
    pub = db.session.query(Publisher).filter_by(name=name).first()
    if pub is None:
        abort(404)
    return render_template("publisher.html", publisher=pub)


@app.route("/character/<name>")
def character(name):
    result = []
    image = db.session.query(Character.image).filter_by(name=name).first()
    real = db.session.query(Character.real).filter_by(name=name).first()
    gender = db.session.query(Character.gender).filter_by(name=name).first()
    publisher_name = db.session.query(Character.publisher_name).filter_by(name=name).first()
    if publisher_name is None:
        abort(404)
    team_sets = db.session.query(characters_teams).filter_by(character_name=name).all()
    vol_sets = db.session.query(characters_volumes).filter_by(character_name=name).all()
    vol_result = []
    for set in vol_sets:
        volume = set[1]
        vol_image = db.session.query(Volume.image).filter_by(name=volume).first()
        temp = {
            'name': volume,
            'image': vol_image
        }
        print(temp)
        vol_result.append(temp)
    team_result = []
    for set in team_sets:
        team = set[1]
        team_image = db.session.query(Team.image).filter_by(name=team).first()
        temp = {
            'name': team,
            'image': team_image
        }
        print(temp)
        team_result.append(temp)

    temp = {
        'name': name,
        'real_name': real,
        'image': image,
        'gender': gender,
        'publisher': publisher_name,
        'teams': team_result,
        'volumes': vol_result
    }
    # print(temp)
    return render_template("character.html", character=temp)


@app.route("/volume/<name>")
def volume(name):
    v = db.session.query(Volume).filter_by(name=name).first()
    if v is None:
        abort(404)
    return render_template("volume.html", volume=v)


@app.route("/team/<name>")
def team(name):
    t = db.session.query(Team).filter_by(name=name).first()
    if t is None:
        abort(404)
    return render_template("team.html", team=t)


@app.route('/api/characters', methods=['GET'])
def characters_api():
    character_name = db.session.query(Character.name).all()
    if character_name is None:
        abort(404)
    result = []
    character_name = list(character_name)
    for character in character_name:
        image = db.session.query(Character.image).filter_by(name=character).first()
        real = db.session.query(Character.real).filter_by(name=character).first()
        gender = db.session.query(Character.gender).filter_by(name=character).first()
        publisher_name = db.session.query(Character.publisher_name).filter_by(name=character).first()
        temp = {
            'name': character,
            'real_name': real,
            'image': image,
            'gender': gender,
            'publisher': publisher_name
        }
        result.append(temp)
    return jsonify({'result': result})


@app.route('/api/publishers', methods=['GET'])
def publishers_api():
    publisher_name = db.session.query(Publisher.name).all()
    result = []
    publisher_name = list(publisher_name)
    for publisher in publisher_name:

        image = db.session.query(Publisher.image).filter_by(name=publisher).first()
        city = db.session.query(Publisher.city).filter_by(name=publisher).first()
        address = db.session.query(Publisher.address).filter_by(name=publisher).first()
        state = db.session.query(Publisher.state).filter_by(name=publisher).first()
        temp = {
            'name': publisher,
            'city': city,
            'image': image,
            'address': address,
            'state': state
        }
        result.append(temp)
    return jsonify({'result': result})


@app.route('/api/volumes', methods=['GET'])
def volumes_api():
    volume_name = db.session.query(Volume.name).all()
    result = []
    volume_name = list(volume_name)
    for volume in volume_name:

        image = db.session.query(Volume.image).filter_by(name=volume).first()
        start = db.session.query(Volume.start_year).filter_by(name=volume).first()
        publisher_name = db.session.query(Volume.publisher_name).filter_by(name=volume).first()
        num_issues = db.session.query(Volume.num_issues).filter_by(name=volume).first()

        temp = {
            'name': volume,
            'publisher': publisher_name,
            'image': image,
            'start_year': start,
            'num_issues': num_issues
        }
        result.append(temp)
    return jsonify({'result': result})


@app.route('/api/teams', methods=['GET'])
def teams_api():

    team_name = db.session.query(Team.name).all()
    result = []
    team_name = list(team_name)
    for team in team_name:

        image = db.session.query(Team.image).filter_by(name=team).first()
        appear = db.session.query(Team.appear).filter_by(name=team).first()
        publisher_name = db.session.query(Team.publisher_name).filter_by(name=team).first()
        num_appearances = db.session.query(Team.num_appearances).filter_by(name=team).first()

        temp = {
            'name': team,
            'publisher': publisher_name,
            'image': image,
            'appear': appear,
            'num_appearances': num_appearances
        }
        result.append(temp)
    return jsonify({'result': result})


@app.route('/api/character/<string:name>', methods=['GET'])
def character_api(name):
    result = []
    real = db.session.query(Character.real).filter_by(name=name).first()
    gender = db.session.query(Character.gender).filter_by(name=name).first()
    publisher_name = db.session.query(Character.publisher_name).filter_by(name=name).first()
    team_sets = db.session.query(characters_teams).filter_by(character_name=name).all()
    vol_sets = db.session.query(characters_volumes).filter_by(character_name=name).all()
    vol_result = []
    #print(db.session.query(Character.image).filter_by(name=name).first())
    for set in vol_sets:
        volume = set[1]
        vol_image = db.session.query(Volume.image).filter_by(name=volume).first()
        temp = {
            'name': volume,
            'image': vol_image
        }
        vol_result.append(temp)
    team_result = []
    for set in team_sets:
        team = set[1]
        team_image = db.session.query(Team.image).filter_by(name=team).first()
        temp = {
            'name': team,
            'image': team_image
        }
        team_result.append(temp)
    temp = {
        'name': name,
        'real_name': real,
        'image': db.session.query(Character.image).filter_by(name=name).first(),
        'gender': gender,
        'publisher': publisher_name,
        'teams': team_result,
        'volumes': vol_result
    }
    #print(temp)
    result.append(temp)
    return jsonify({'result': result})


@app.route('/api/publisher/<string:name>', methods=['GET'])
def publisher_api(name):
    publisher = db.session.query(Publisher).filter_by(name=name).first()
    if not publisher:
        abort(400)

    return jsonify({'result': publisher.json_it()})


@app.route('/api/volume/<string:name>', methods=['GET'])
def volume_api(name):
    volume = db.session.query(Volume).filter_by(name=name).first()

    if not volume:
        abort(400)

    return jsonify({'result': volume.json_it()})


@app.route('/api/team/<string:name>', methods=['GET'])
def team_api(name):
    team = db.session.query(Team).filter_by(name=name).first()

    if not team:
        abort(400)

    return jsonify({'result': team.json_it()})



@app.route('/search/<name>')
def search(name):
    name = name.lower()
    queries = name.split() # makes an array
    print(queries)
    tup = ()

    a = and_(Character.tsvector_col.match(q) for q in queries)
    o = or_(Character.tsvector_col.match(q) for q in queries)
    #achar = and_(*tup)
    #ochar = or_(tup)
    a_string = ''
    for index in range(0, len(queries)):
        a_string += queries[index]
        if index + 1 is not len(queries):
            a_string += ' & '
    print(a_string)
    o_string = ''
    for index in range(0, len(queries)):
        o_string += queries[index]
        if index + 1 is not len(queries):
            o_string += ' | '
    print(o_string)

    acharacters = db.session.query(Character, func.ts_headline('english', Character.name, func.to_tsquery(a_string)).label('hname'), func.ts_headline('english', Character.publisher_name, func.plainto_tsquery(a_string)).label('hpub'), func.ts_headline('english', Character.appear, func.plainto_tsquery(a_string)).label('happear')).filter(and_(Character.tsvector_col.match(q) for q in queries)).all()

    ocharacters = db.session.query(Character, func.ts_headline('english', Character.name, func.to_tsquery(o_string)).label('hname'), func.ts_headline('english', Character.publisher_name, func.plainto_tsquery(o_string)).label('hpub'), func.ts_headline('english', Character.appear, func.plainto_tsquery(o_string)).label('happear')).filter(or_(Character.tsvector_col.match(q) for q in queries)).all()

    apublishers = db.session.query(Publisher, func.ts_headline('english', Publisher.state, func.to_tsquery(a_string)).label('hstate'), func.ts_headline('english', Publisher.name, func.to_tsquery(a_string)).label('hname'), func.ts_headline('english', Publisher.address, func.plainto_tsquery(a_string)).label('haddress'), func.ts_headline('english', Publisher.city, func.plainto_tsquery(name)).label('hcity')).filter(and_(Publisher.tsvector_col.match(q) for q in queries)).all()
    opublishers = db.session.query(Publisher, func.ts_headline('english', Publisher.state, func.to_tsquery(o_string)).label('hstate'), func.ts_headline('english', Publisher.name, func.to_tsquery(o_string)).label('hname'), func.ts_headline('english', Publisher.address, func.plainto_tsquery(o_string)).label('haddress'), func.ts_headline('english', Publisher.city, func.plainto_tsquery(name)).label('hcity')).filter(or_(Publisher.tsvector_col.match(q) for q in queries)).all()
    ateams = db.session.query(Team, func.ts_headline('english', Team.name, func.to_tsquery(a_string)).label('hname'), func.ts_headline('english', Team.publisher_name, func.plainto_tsquery(a_string)).label('hpub'), func.ts_headline('english', Team.appear, func.plainto_tsquery(a_string)).label('happear')).filter(and_(Team.tsvector_col.match(q) for q in queries)).all()
    oteams = db.session.query(Team, func.ts_headline('english', Team.name, func.to_tsquery(o_string)).label('hname'), func.ts_headline('english', Team.publisher_name, func.plainto_tsquery(o_string)).label('hpub'), func.ts_headline('english', Team.appear, func.plainto_tsquery(o_string)).label('happear')).filter(or_(Team.tsvector_col.match(q) for q in queries)).all()
    avolumes = db.session.query(Volume, func.ts_headline('english', Volume.name, func.to_tsquery(a_string)).label('hname'), func.ts_headline('english', Volume.publisher_name, func.plainto_tsquery(a_string)).label('hpub'), func.ts_headline('english', Volume.start_year, func.plainto_tsquery(a_string)).label('hstart')).filter(and_(Volume.tsvector_col.match(q) for q in queries)).all()
    ovolumes = db.session.query(Volume, func.ts_headline('english', Volume.name, func.to_tsquery(o_string)).label('hname'), func.ts_headline('english', Volume.publisher_name, func.plainto_tsquery(o_string)).label('hpub'), func.ts_headline('english', Volume.start_year, func.plainto_tsquery(o_string)).label('hstart')).filter(or_(Volume.tsvector_col.match(q) for q in queries)).all()

    #print(publishers)
    #print(teams)
    #print(volumes)
    return render_template('search_result_template.html',  acharacters=acharacters, ocharacters=ocharacters, opublishers=opublishers, apublishers=apublishers, avolumes=avolumes, ovolumes=ovolumes, ateams=ateams, oteams=oteams)

@app.route('/visual')
def visual():
    return render_template('visual.html')
def add_publishers():
    db.create_all()
    for publisher in PublisherName:
        print(publisher)
        print(dir + "/database/publishers/" + publisher)
        os.chdir(dir + "/database/publishers/" + publisher)
        for data in glob.glob('*.json'):
            f = open(dir + 'database/publishers/' + publisher + '/' + publisher + '.json', 'r')
        test = json.load(f)
        pub = {
            'name': test['name'],
            'address': test['location']['address'],
            'city': test['location']['city'],
            'state': test['location']['state'],
            'deck': test['deck'],
            'image': test['image']
        }
        pub = Publisher(**pub)

        try:
            db.session.add(pub)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()



def add_teams():
    db.create_all()
    for publisher in PublisherName:
        if publisher is not None:

            os.chdir(dir + "database/publishers/" + publisher + '/team')
            for data in glob.glob('*.json'):
                f = open(data, 'r')
                test = json.load(f)
                if 'appear' not in test.keys():
                    test['appear'] = 'Unknown'
                #pprint(test)
                pub = {
                    'name': test['name'],
                    'num_appearances': test['num_appearances'],
                    'description': test['description'],
                    'image': test['image'],
                    'appear': test['appear'],
                    'publisher_name': publisher
                }
                pub = Team(**pub)

                try:
                    db.session.add(pub)
                    db.session.commit()
                except:
                    db.session.rollback()
                    raise
                finally:
                    db.session.close()
            test = {}


def add_teams_volumes():
    db.create_all()
    for publisher in PublisherName:
        # pprint([x[0] for x in os.walk(dir + "database/publishers/" + publisher + '/')])
        # pprint([x[0] for x in os.walk(dir + "database/publishers/" + publisher + '/')])
        # os.chdir(dir + "database/publishers/" + publisher)
        teams = (os.listdir(dir + "database/publishers/" + publisher + '/'))
        for team in teams:
            if team != 'team' and not ('json' in team):
                # print(publisher + '   ' + team)
                characters = (os.listdir(dir + "database/publishers/" + publisher + '/' + team))
                for character in characters:
                    # this character is partk of this publisher and team
                    if character == 'Team Volumes':
                        print('VOLUME')
                        team_volumes = (
                            os.listdir(dir + "database/publishers/" + publisher + '/' + team + '/' + character))
                        for volume in team_volumes:
                            os.chdir(
                                dir + "database/publishers/" + publisher + '/' + team + '/Team Volumes/' + volume)
                            vol_json = {}
                            for data in glob.glob('*.json'):
                                f = open(data, 'r')
                                vol_json = json.load(f)
                            # print('BOOOOOM')
                            # we can assign volume to team, volume to publisher, volume to characters, team to characters, and character to publisher
                            characters = [character for character in characters if
                                          (character != 'Team Volumes' and 'json' not in character)]
                            # print('volume: ' + volume + ' team: ' + team + ' publisher: ' + publisher + ' characters: ')
                            print(characters)
                            print('kk')
                            assign_volume_publisherandteams(vol_json, publisher, team)
                            # assign_volume_team(volume, team)
                            for character in characters:
                                os.chdir(dir + "database/publishers/" + publisher + '/' + team + '/' + character)
                                char_json = {}
                                for data in glob.glob('*.json'):
                                    f = open(data, 'r')
                                    char_json = json.load(f)
                                assign_character_publisherteamsandvolumes(char_json, publisher, team, volume)
                                # print('BOOOOOOOM')
                        break


def assign_volume_publisherandteams(volume, publisher, team):
    temp = fetch_json(volume['api_url'] + '?api_key=d1fcd2dc19ac4cbac24fd26d5161210b150cbaed&format=json')
    if volume['description'] is None:
        volume['description'] = 'None'
    result = {
        'image': temp['results']['image']['small_url'],
        'description': volume['description'],
        'start_year': str(volume['start_year']),
        'name': volume['name'],
        'num_issues': str(volume['count_of_issues']),
        'publisher_name': publisher,
    }
    print(result)
    with db.session.no_autoflush:
        volume_obj = db.session.query(Volume).filter_by(name=volume['name']).first()
        team_obj = db.session.query(Team).filter_by(name=team).first()
        if volume_obj is not None and team_obj is not None:
            print('volume Object')
            # print(volume_obj)
            volume_obj.volume_teams.append(team_obj)
            # print(volume_obj)
            db.session.commit()
            # commit here
        else:
            result = Volume(**result)
            if team_obj is not None:
                result.volume_teams.append(team_obj)
                db.session.add(result)
                db.session.commit()
        db.session.close()


def assign_character_publisherteamsandvolumes(character, publisher, team, volume):
    print(character)
    # temp = fetch_json(volume['api_url'] + '?api_key=d1fcd2dc19ac4cbac24fd26d5161210b150cbaed&format=json')
    if character['gender'] is 1:
        character['gender'] = 'Male'
    elif character['gender'] is 2:
        character['gender'] = 'Female'
    else:
        character['gender'] = 'Other'
    if character['birth'] is None:
        character['birth'] = 'Unknown'
    if 'appear' not in character.keys():
        character['appear'] = 'Unknown'
    if character['creator'] is None or 'name' not in character['creator'].keys():
        name = 'Unknown'
    elif type(character['creator']) is str:
        name = character['creator']
    else:
        name = character['creator']['name']

    result = {
        'image': character['image'],
        'birth': character['birth'],
        'name': character['name'],
        'creator': name,
        'num_appearances': str(character['num_appearances']),
        'publisher_name': publisher,
        'appear': character['appear'],
        'gender': character['gender'],

    }
    # print(result)
    char_obj = db.session.query(Character).filter_by(name=character['name']).first()
    volume_obj = db.session.query(Volume).filter_by(name=volume).first()
    team_obj = db.session.query(Team).filter_by(name=team).first()
    if char_obj is not None and team_obj is not None:
        print('Character Object')
        # print(volume_obj)
        char_obj.character_teams.append(team_obj)
        char_obj.character_volumes.append(volume_obj)
        # print(volume_obj)
        db.session.commit()
        # commit here
    else:
        result = Character(**result)
        if team_obj is not None:
            result.character_teams.append(team_obj)
            result.character_volumes.append(volume_obj)
            db.session.add(result)
    db.session.commit()
    db.session.close()



def fetch_json(url):
    assert isinstance(url, str), "the URL must be a string"
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        return None
    content = response.read().decode("utf8")
    data = json.loads(content)
    assert isinstance(data, dict), "response was not a json"
    return data


def team_to_json(obj):
    c = []
    for char in obj.team_characters:
        c += {'name': char.name, 'image': char.image}
    v = []
    for volume in obj.team_volumes:
        v += {'name': volume.name, 'image': volume.image}

    ans = {
        'appear': obj['appear'],
        'description': obj['description'],
        'image': obj['image'],
        'name': obj['name'],
        'num_appearances': obj['num_appearances'],
        'publisher_name': obj['publisher_name'],
        'image': obj['image'],
        'num_appearances': obj['num_appearances'],
        'team_characters': c,
        'team_volumes': v
    }
    return ans


def volume_to_json(obj):
    t = []
    for team in obj.character_teams:
        t += {'name': team.name, 'image': team.image}
    c = []
    for character in obj.character_volumes:
        c += {'name': volume.name, 'image': volume.image}

    ans = {
        'description': obj['description'],
        'image': obj['image'],
        'name': obj['name'],
        'num_issues': obj['num_issues'],
        'publisher_name': obj['publisher_name'],
        'start_year': obj['start_year'],
        'volume_teams': t,
        'volume_characters': c
    }
    return ans


if __name__ == '__main__':
    # test = db.session.query(Publisher).filter_by(name='Vertigo').one()
    # print(test.publisher_characters)
    # for character in test.publisher_characters:
    #    print(character.name)
    # test = db.session.query(Character).filter_by(name='The Sandman')
    # test = db.session.query(Volume).filter_by(name='100 Bullets')

    #add_publishers()
    #add_teams()
    #add_teams_volumes()
    test = db.session.query(Publisher).filter_by(name='Vertigo')
    # update_publisher_teams()
    app.run(debug=True)
