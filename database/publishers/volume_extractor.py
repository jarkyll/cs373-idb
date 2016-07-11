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
# os.chdir("/u/cz4792/cs373/cs373-idb/database/results")
postpend = "?api_key=d1fcd2dc19ac4cbac24fd26d5161210b150cbaed&format=json"
id = 0
PublisherName = ['Aftershock Comics', 'Boom! Studios', 'Dark Horse Comics', 'Dell', 'Fiction House', 'IDW Publishing', 'Image', 'Top Cow', 'Valiant', 'Vertigo']
dir = os.getcwd() + '/'

f = open(dir + 'results/team_results7-10.json', 'r')
test = json.load(f)
for id in test.keys():
    volumeCount = 0
    team_url = test[str(id)]['api_url']
    # if int(id)/10 == 0:
    pathName = PublisherName[int(id) // 10]

    info = fetch_json(team_url + postpend)

    if info and info['results']['volume_credits']:
        volumeList = info['results']['volume_credits']

        for volume in volumeList:
            extracted = {}
            extracted['id'] = int(id) * 100 + volumeCount
            extracted['name'] = volume['name']
            if '/' in extracted['name']:
                extracted['name'] = extracted['name'].replace('/', '_')
            extracted['api_url'] = volume['api_detail_url']

            info2 = fetch_json(volume['api_detail_url'] + postpend)
            if info2 and info2['results']['deck']:
                extracted['description'] = info2['results']['deck']
            else:
                extracted['description'] = None
            if info2 and info2['results']['count_of_issues']:
                extracted['count_of_issues'] = info2['results']['count_of_issues']
            else:
                extracted['count_of_issues'] = None

            if info2 and info2['results']['start_year']:
                extracted['start_year'] = info2['results']['start_year']
            else:
                extracted['start_year'] = None

            volumeCount += 1
            if volumeCount == 3:
                break

            result[int(id) * 100 + volumeCount - 1] = extracted

            direc1 = dir + pathName + '/' + test[str(id)]['name'] + '/Team Volumes'
            if not os.path.exists(direc1):
                os.mkdir(direc1)


            direc = dir + pathName + '/' + test[str(id)]['name'] + '/Team Volumes/' + extracted['name']
            if not os.path.exists(direc):
                os.mkdir(direc)
            path = direc + '/' + extracted['name'] + '.json'
            with open(path, 'w') as f:
                json.dump(extracted, f, indent=4)

            f.close()
    else:
        continue

f.close()

with open(dir + "results/volume_results7-10.json", 'w') as f:
    json.dump(result, f, indent=4)

f.close()

