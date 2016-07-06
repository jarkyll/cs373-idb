#!/usr/bin/env python

import os, glob
import json
from pprint import pprint


result = {}
os.chdir("C:/Users/Nabeel/Documents/Frontend")
id = 0
for data in glob.glob("*.json"):
    extracted = {}
    f = open(data, 'r')
    test = json.load(f)
    #pprint(test['number_of_total_results'])

    pprint(data)
    pprint(test.keys())
    extracted['name'] = test['results']['name']
    extracted['location'] = {}
    extracted['location']['city'] = test['results']['location_city']
    extracted['location']['state'] = test['results']['location_state']
    extracted['location']['address'] = test['results']['location_address']
    extracted['deck'] = test['results']['deck']
    extracted['characters'] = test['results']['characters']
    extracted['volumes'] = test['results']['volumes']
    extracted['teams'] = test['results']['teams']
    extracted['image'] = test['results']['image']
    result[id] = extracted
    f.close()
    id += 1

with open("results/publisher_results.json", 'w') as f:
    json.dump(result, f, indent=4)

f = open('results/publisher_results.json', 'r')
pprint(json.load(f))
f.close()
