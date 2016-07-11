#!/usr/bin/env python

import os, glob
import json
from pprint import pprint

postpend = "?api_key=d1fcd2dc19ac4cbac24fd26d5161210b150cbaed&format=json"

result = {}
os.chdir('/u/cz4792/cs373/cs373-idb/database/publishers')
id = 0
for data in glob.glob('*.json'):
    extracted = {}
    f = open(data, 'r')
    test = json.load(f)

    extracted['id'] =  id
    extracted['name'] = test['results']['name']
    extracted['location'] = {}
    extracted['location']['city'] = test['results']['location_city']
    extracted['location']['state'] = test['results']['location_state']
    extracted['location']['address'] = test['results']['location_address']
    extracted['deck'] = test['results']['deck']
    extracted['teams'] = test['results']['teams']
    if test['results']['image'] != None:
        extracted['image'] = test['results']['image']['small_url'] + postpend
    else:
        extracted['image'] = None
    result[id] = extracted
    f.close()
    id += 1

    direc = '/u/cz4792/cs373/cs373-idb/database/publishers/' + extracted['name']
    if not os.path.exists(direc):
        os.mkdir('/u/cz4792/cs373/cs373-idb/database/publishers/' + extracted['name'])
    path = '/u/cz4792/cs373/cs373-idb/database/publishers/' + extracted['name'] + '/' + extracted['name'] + '.json'
    with open(path, 'w') as f:
        json.dump(extracted, f, indent=4)

    f.close()

with open('/u/cz4792/cs373/cs373-idb/database/results/publisher_results.json', 'w') as f:
    json.dump(result, f, indent=4)

f.close()
