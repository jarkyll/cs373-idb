#!/usr/bin/env python

import os, glob
import json
import urllib.request
from pprint import pprint


def fetch_json(url):
    assert isinstance(url, str), "the URL must be a string"
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        print(url)
    content = response.read().decode("utf8")
    data = json.loads(content)
    assert isinstance(data, dict), "response was not a json"
    return data

result = {}
#os.chdir("/u/cz4792/cs373/cs373-idb/database/results")
postpend = "?api_key=d1fcd2dc19ac4cbac24fd26d5161210b150cbaed&format=json"
dir = os.getcwd() + '/'
id = 0

<<<<<<< HEAD:database/publishers/team_extractor.py
PublisherName = ['Aftershock Comics', 'Boom! Studios', 'Dark Horse Comics', 'Dell', 'Fiction House', 'IDW Publishing', 'Image', 'Top Cow', 'Valiant', 'Vertigo']
=======
PublisherName = ['Aftershock Comics', 'Boom! Studios', 'Dark Horse Comics', 'Dell', 'Fiction House']
>>>>>>> ee263c87dd2a660575ffa50f44a29acb3bfe5608:database/teams/team_extractor.py

f = open(dir + 'results/publisher_results.json', 'r')
test = json.load(f)
<<<<<<< HEAD:database/publishers/team_extractor.py
for id in range(6, 10, 1):
=======
for id in range(3, 5):
>>>>>>> ee263c87dd2a660575ffa50f44a29acb3bfe5608:database/teams/team_extractor.py
    teamCount = 0
    teamList = []
    teamList = test[str(id)]['teams']
    for team in teamList:
        extracted = {}
        extracted['id'] = id * 10 + teamCount
        extracted['name'] = team['name']
        team_url = team['api_detail_url']
        extracted['api_url'] = team_url
        info = fetch_json(team_url + postpend)
        

        if info['results']['image']:
            extracted['image'] = info['results']['image']['small_url']
        else:
            extracted['image'] = None

        teamCount += 1
        if teamCount == 11:
            break

        result[id * 10 + teamCount - 1] = extracted

        direc = dir + PublisherName[id] + '/' + extracted['name']
        if not os.path.exists(direc):
            os.mkdir(direc)
        path = direc + '/' + extracted['name'] + '.json'
        with open(path, 'w') as f:
            json.dump(extracted, f, indent=4)

        f.close()
    
f.close()


<<<<<<< HEAD:database/publishers/team_extractor.py
with open( dir + "results/team_results7-10.json", 'w') as f:
=======
with open("/u/cz4792/cs373/cs373-idb/database/results/team_results4-5.json", 'w') as f:
>>>>>>> ee263c87dd2a660575ffa50f44a29acb3bfe5608:database/teams/team_extractor.py
    json.dump(result, f, indent=4)

f.close()

