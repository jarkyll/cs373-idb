#!/usr/bin/env python

import os, glob
import json
import urllib.request
from pprint import pprint

postpend = "?api_key=f7d2be7e2a7080255f1b040214cd344b372cda4c&format=json"

def fetch_volumes(publisher):
    results = {}
    id = 0
    volumes_url = [ volume['api_detail_url'] for volume in publisher['volumes']]
    print(len(volumes_url))
    for url in volumes_url:
        volume = {}
        info = fetch_json(url + postpend)
        info = info['results']
        volume['name'] = info['name']
        volume['image'] = info['image']
        volume['publisher'] = info['publisher']
        volume['characters'] = info['characters']
        volume['aliases'] = info['aliases']
        volume['description'] = info['description']
        results[id] = volume
        id += 1
        if(id == 10):
            break
    assert results is not {}
    return results



def fetch_teams(publisher):
    results = {}
    id = 0
    teams_url = [ team['api_detail_url'] for team in publisher['teams']]
    print(len(teams_url))
    for url in teams_url:
        team = {}
        info = fetch_json(url + postpend)
        info = info['results']
        team['name'] = info['name']
        team['image'] = info['image']
        team['publisher'] = info['publisher']
        team['characters'] = info['characters']
        team['aliases'] = info['aliases']
        team['description'] = info['description']
        team['allies'] = info['character_friends']
        team['enemies'] = info['character_enemies']
        results[id] = team
        id += 1
        if(id == 10):
            break
    assert results is not {}
    return results




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
# now get all of Dark Horse Comics teams, characters, and that is it
if __name__ == '__main__':
    os.chdir("C:/Users/Nabeel/Documents/Frontend/results")
    f = open("publisher_results.json", "r")
    publishers = json.load(f)
    for publisher in publishers:
        pub_info = publishers[publisher]
        volumes = fetch_volumes(pub_info)
        with open(pub_info['name']+" volumes.json", 'w') as f:
            json.dump(volumes, f, indent=4)
        teams = fetch_teams(pub_info)
        with open(pub_info['name']+" teams.json", 'w') as f:
            json.dump(teams, f, indent=4)
# to fetch characters, we want to go through every volume and team
    fetch_characters()
