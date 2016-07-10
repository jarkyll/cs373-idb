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
os.chdir("/u/cz4792/cs373/cs373-idb/database/results")
postpend = "?api_key=d1fcd2dc19ac4cbac24fd26d5161210b150cbaed&format=json"
id = 0
count = 0

f = open('team_results.json', 'r')
test = json.load(f)
for id in test.keys():
    characterCount = 0
    team_url = test[str(id)]['api_url']

    info = fetch_json(team_url + postpend)

    if info and info['results']['characters']:
        characterList = info['results']['characters']


        for character in characterList:
            count += 1
            print(count)
            extracted = {}
            extracted['id'] = int(id) * 10 + characterCount
            extracted['name'] = character['name']
            # pprint(extracted['name'])
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

            creator = {}
            if info2 and info2['results']['creators']:    
                creatorList = info2['results']['creators']
                for creatorDict in creatorList:
                    creator['name'] = creatorDict['name']

            extracted['creator'] = creator

            characterCount += 1
            if characterCount == 4:
                break

            result[int(id) * 10 + characterCount - 1] = extracted
    else:
        continue
    
f.close()


with open("/u/cz4792/cs373/cs373-idb/database/results/character_results.json", 'w') as f:
    json.dump(result, f, indent=4)

f = open('/u/cz4792/cs373/cs373-idb/database/results/character_results.json', 'r')
f.close()

