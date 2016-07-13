from flask import Flask, render_template, jsonify, abortgit
from app.demo import *
import jinja2
from test_suite import *
import unittest, sys



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




@app.route("/")
def homepage():
    return render_template("index.html")
'''
@app.route('/runtests')
def runtests():
    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream)
    result = runner.run(unittest.makeSuite(MyTests))
    print(result, file=sys.stderr)
    return result
'''
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
    return render_template("publisher.html", publisher=pub)


@app.route("/character/<name>")
def character(name):
    char = db.session.query(Character).filter_by(name=name).first()
    return render_template("publisher.html", character=char)


@app.route("/volume/<name>")
def volume(name):
    v = db.session.query(Volume).filter_by(name=name).first()
    return render_template("planet.html", volume=v)


@app.route("/team/<name>")
def team(name):
    t = db.session.query(Team).filter_by(name=name).first()
    return render_template("space.html", team=t)


@app.route('/api/characters', methods=['GET'])
def characters_api():
    character_name = db.session.query(Character.name).all()
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
    image = db.session.query(Character.image).filter_by(name=name).first()
    real = db.session.query(Character.real).filter_by(name=name).first()
    gender = db.session.query(Character.gender).filter_by(name=name).first()
    publisher_name = db.session.query(Character.publisher_name).filter_by(name=name).first()
    team_sets = db.session.query(characters_teams).filter_by(character_name=name).all()
    vol_sets = db.session.query(characters_volumes).filter_by(character_name=name).all()
    vol_result = []
    for set in vol_sets:
        volume = set[1]
        image = db.session.query(Volume.image).filter_by(name=volume).first()
        temp = {
            'name': volume,
            'image': image
        }
        print(temp)
        vol_result.append(temp)
    team_result = []
    for set in team_sets:
        team = set[1]
        image = db.session.query(Team.image).filter_by(name=team).first()
        temp = {
            'name': team,
            'image': image
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


def add_publishers():
    db.create_all()
    for publisher in PublisherName:
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
    '''
    pub = (**DEMO)

    try:
        db.session.add(pub)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
    '''


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
                pprint(test)
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
        'start_year': int(volume['start_year']),
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
        character['gender'] = 'Female'
    elif character['gender'] is 1:
        character['gender'] = 'Male'
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
    '''
    try:
        db.session.add(result)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    '''


def fetch_json(url):
    assert isinstance(url, str), "the URL must be a string"
    response = urllib.request.urlopen(url).read().decode("utf8")
    data = json.loads(response)
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
