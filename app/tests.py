from unittest import main, TestCase
import os, glob

from models import *


class MyTests(TestCase):



    def test_publisher_name(self):
        res = fetch_json('http://downing.rocks/api/publisher/Vertigo')
        self.assertEqual('Vertigo', res["name"])

    
    def test_publisher_image(self):
        res = fetch_json('http://downing.rocks/api/publisher/Vertigo')
        self.assertEqual("http://static3.comicvine.com/uploads/scale_small/6/67663/4717683-logo.jpg?api_key=d1fcd2dc19ac4cbac24fd26d5161210b150cbaed&format=json", res["image"])
    
    def test_publisher_city(self):
        res = fetch_json('http://downing.rocks/api/publisher/Vertigo')
        self.assertEqual("New York City", res["city"])

    def test_publisher_teams(self):
        res = fetch_json('http://downing.rocks/api/publisher/Vertigo')
        self.assertEqual("The Losers", res["teams"][0])

    def test_character_name(self):
        res = fetch_json('http://downing.rocks/api/character/DeBlanc')
        self.assertEqual("DeBlanc", res["name"])

    def test_character_real_name(self):
        res = fetch_json('http://downing.rocks/api/character/DeBlanc')
        self.assertEqual("DeBlanc", res["real"])

    def test_character_name2(self):
        res = fetch_json('http://downing.rocks/api/character/Granny')
        self.assertEqual("Granny", res["name"])

    def test_team_name(self):
        res = fetch_json('http://downing.rocks/api/teams/Adephi')
        self.assertEqual("Adephi", res["name"])

    def test_team_description(self):
        res = fetch_json('http://downing.rocks/api/teams/Adephi')
        self.assertEqual(" ", res["description"])
    
    def test_team_num_appear(self):
        res = fetch_json('http://downing.rocks/api/teams/Adephi')
        self.assertEqual(0, res["num_appearances"])

    def test_team_image(self):
        res = fetch_json('http://downing.rocks/api/teams/Adephi')
        self.assertEqual(None, res["image"])

    def test_volume_name(self):
        res = fetch_json('http://downing.rocks/api/volumes/Preacher')
        self.assertEqual("Preacher", res["name"])

    def test_volume_description(self):
        res = fetch_json('http://downing.rocks/api/volumes/Preacher')
        self.assertEqual(None, res["description"])

    def test_volume_num_issues(self):
        res = fetch_json('http://downing.rocks/api/volumes/Preacher')
        self.assertEqual(66, res["num_issues"])

    def fetch_json(url):
        assert isinstance(url, str), "the URL must be a string"
        try:
            response = urllib.request.urlopen(url)
        except urllib.error.HTTPError:
            return None
        content = response.read().decode("utf8")
        data = json.loads(content)
        assert isinstance(data, dict), "response was not a json"
        return data
        
if __name__ == "__main__":
    main()