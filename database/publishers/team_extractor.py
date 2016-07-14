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

PublisherName = ['Aftershock Comics', 'Boom! Studios', 'Dark Horse Comics', 'Dell', 'Fiction House', 'IDW Publishing', 'Image', 'Top Cow', 'Valiant', 'Vertigo']

f = open(dir + 'results/publisher_results.json', 'r')
test = json.load(f)

for id in range(6, 10):
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
        extracted['description'] = info['results']['deck']
        if info['results']['image']:
            extracted['image'] = info['results']['image']['small_url']
        else:
            extracted['image'] = None
        if info['results']['first_appeared_in_issue']:
            if info['results']['first_appeared_in_issue']['name'] is not None:
                extracted['appear'] = info['results']['first_appeared_in_issue']['name']
            else:
                extracted['appear'] = 'Unknown'
        if 'count_of_isssue_appearances' in info['results'].keys():
            extracted['num_appearances'] = info['results']['count_of_isssue_appearances']
        else:
            extracted['num_appearances'] = info['results']['count_of_isssue_appearances']


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


with open( dir + "results/team_results7-10.json", 'w') as f:
    json.dump(result, f, indent=4)

f.close()

