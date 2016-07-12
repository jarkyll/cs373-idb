import glob
import json
import os
import urllib.request
from pprint import pprint
from unit_models import *
from app.demo import *

PublisherName = ['Vertigo', 'IDW Publishing', 'Dark Horse Comics', 'Top Cow', 'Valiant', 'Dell', 'Aftershock Comics',
                 'Image', 'Fiction House', 'Boom! Studios']
dir = os.getcwd() + '/'


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
                            #print('volume: ' + volume + ' team: ' + team + ' publisher: ' + publisher + ' characters: ')
                            print(characters)
                            print('kk')
                            assign_volume_publisherandteams(vol_json, publisher, team)
                            #assign_volume_team(volume, team)
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
            #print(volume_obj)
            volume_obj.volume_teams.append(team_obj)
            #print(volume_obj)
            db.session.commit()
            #commit here
        else:
            result = Volume(**result)
            if team_obj is not None:
                result.volume_teams.append(team_obj)
                db.session.add(result)
                db.session.commit()
        db.session.close()

def assign_character_publisherteamsandvolumes(character, publisher, team, volume):
    print(character)
    #temp = fetch_json(volume['api_url'] + '?api_key=d1fcd2dc19ac4cbac24fd26d5161210b150cbaed&format=json')
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
    #print(result)
    char_obj = db.session.query(Character).filter_by(name=character['name']).first()
    volume_obj = db.session.query(Volume).filter_by(name=volume).first()
    team_obj = db.session.query(Team).filter_by(name=team).first()
    if char_obj is not None:
        print('Character Object')
        #print(volume_obj)
        char_obj.character_teams.append(team_obj)
        char_obj.character_volumes.append(volume_obj)
        #print(volume_obj)
        db.session.commit()
            #commit here
    else:
        result = Character(**result)
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


def assign_character_publisher(character, publisher):
    pass


def assign_character_team(character, team):
    pass


def assign_character_volume(character, volume):
    pass


def fetch_json(url):
    assert isinstance(url, str), "the URL must be a string"
    response = urllib.request.urlopen(url).read().decode("utf8")
    data = json.loads(response)
    assert isinstance(data, dict), "response was not a json"
    return data

if __name__ == '__main__':
    #test = db.session.query(Publisher).filter_by(name='Vertigo').one()
    #print(test.publisher_characters)
    #for character in test.publisher_characters:
    #    print(character.name)
    #test = db.session.query(Character).filter_by(name='The Sandman')
    #test = db.session.query(Volume).filter_by(name='100 Bullets')

    add_publishers()
    add_teams()
    add_teams_volumes()
    test = db.session.query(Publisher).filter_by(name='Vertigo')
    # update_publisher_teams()
    app.run()
