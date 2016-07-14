#!/usr/bin/env python

import os, glob
import json
import urllib.request
from pprint import pprint


def fetch_json(url):
    assert isinstance(url, str), "the URL must be a string"
    # response = urllib.request.urlopen('http://python.org/')
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        print(url)
        return None
    content = response.read().decode("utf8")
    data = json.loads(content)
    assert isinstance(data, dict), "response was not a json"
    return data

result = {}
#os.chdir("/u/cz4792/cs373/cs373-idb/database/results")
postpend = "?api_key=bbb45e4e4bada96b673ed52a3fe5e27d94a548fb&format=json"
id = 0
PublisherName = ['Aftershock Comics', 'Boom! Studios', 'Dark Horse Comics', 'Dell', 'Fiction House', 'IDW Publishing', 'Image', 'Top Cow', 'Valiant', 'Vertigo']
dir = os.getcwd() + '/'

f = open(dir + 'results/team_results1-3.json', 'r')
test = json.load(f)
for id in test.keys():
    characterCount = 0
    team_url = test[str(id)]['api_url']
    pathName = PublisherName[int(id)//10]

    info = fetch_json(team_url + postpend)

    if info and info['results']['characters']:
        characterList = info['results']['characters']


        for character in characterList:
            extracted = {}
            extracted['id'] = int(id) * 10 + characterCount
            extracted['name'] = character['name']
            extracted['api_url'] = character['api_detail_url']

            
            info2 = fetch_json(character['api_detail_url'] + postpend)
            if info2 and info2['results']['birth']:
                extracted['birth'] = info2['results']['birth']
            else:
                extracted['birth'] = None
            if info2 and info2['results']['gender']:
                extracted['gender'] = info2['results']['gender']
            else:
                extracted['gender'] = None

            if info2 and info2['results']['image']:
                extracted['image'] = info2['results']['image']['small_url']
            else:
                extracted['image'] = None
            if info2 and info2['results']['first_appeared_in_issue']:
                if info2['results']['first_appeared_in_issue']['name']:
                    extracted['appear'] = info2['results']['first_appeared_in_issue']['name']
            else:
                extracted['appear'] = None
            if info2 and info2['results']['count_of_issue_appearances']:
                extracted['num_appearances'] = info2['results']['count_of_issue_appearances']
            else:
                extracted['num_appearances'] = 0
            if info2 and info2['results']['real_name']:
                extracted['real_name'] = info2['results']['real_name']
            else:
                extracted['real_name'] = 'Unknown'

            creator = {}
            if info2 and info2['results']['creators']:    
                creatorList = info2['results']['creators']
                for creatorDict in creatorList:
                    creator['name'] = creatorDict['name']

            extracted['creator'] = creator

            characterCount += 1
            if characterCount == 6:
                break

            result[int(id) * 10 + characterCount - 1] = extracted

            direc = dir + pathName + '/' + test[str(id)]['name'] + '/' + extracted['name']
            if not os.path.exists(direc):
                os.mkdir(direc)
            path = direc + '/' + extracted['name'] + '.json'
            with open(path, 'w') as f:
                json.dump(extracted, f, indent=4)

            f.close()




    else:
        continue
    
f.close()


with open(dir + "results/character_results1-3.json", 'w') as f:
    json.dump(result, f, indent=4)

f.close()

