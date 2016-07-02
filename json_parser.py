#!/usr/bin/env python

import os, glob
import json
import urllib.request
from pprint import pprint
postpend = "?api_key=b758828080feaa39ca40e1801ec2452eceaf6a9d&format=json"
f = open("results.json", 'r')

response = json.load(f)

publisher = response['3']

volumes_url = [ volume['api_detail_url'] for volume in publisher['volumes']]
print(len(volumes_url))
# fetches the list of volumes
id = 0
results = {}
for url in volumes_url:
    volume = {}
    url += postpend
    #req = request.Request(url)
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf8')
    data = json.loads(content)
    data = data['results']
    volume['name'] = data['name']
    volume['image'] = data['image']
    volume['publisher'] = data['publisher']
    volume['characters'] = data['characters']
    volume['aliases'] = data['aliases']
    volume['description'] = data['description']
    #pprint(volume)
    results[id] = volume
    id += 1
pprint(results)
print(len(volumes_url))

with open("testresults.json", 'w') as f:
    json.dump(results, f, indent=4)
# now get all of Dark Horse Comics teams, characters, and that is it
