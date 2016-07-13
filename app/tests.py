from unittest import main, TestCase
import urllib.request
import json


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


class MyTests(TestCase):
    def test_publisher_name(self):
        res = fetch_json('http://downing.rocks/api/publisher/Vertigo')
        self.assertEqual('Vertigo', res["result"]["name"])

    def test_publisher_image(self):
        res = fetch_json('http://downing.rocks/api/publisher/Vertigo')
        self.assertEqual(
            "http://static3.comicvine.com/uploads/scale_small/6/67663/4717683-logo.jpg?api_key=d1fcd2dc19ac4cbac24fd26d5161210b150cbaed&format=json",
            res["result"]["image"])

    def test_publisher_city(self):
        res = fetch_json('http://downing.rocks/api/publisher/Vertigo')
        self.assertEqual("New York City", res["result"]["city"])

    def test_publisher_teams(self):
        res = fetch_json('http://downing.rocks/api/publisher/Vertigo')
        self.assertEqual("The Losers", res["result"]["publisher_teams"][1]["name"])

    def test_character_name(self):
        res = fetch_json('http://downing.rocks/api/character/DeBlanc')
        self.assertEqual("DeBlanc", res["result"][0]["name"])

    def test_character_real_name(self):
        res = fetch_json('http://downing.rocks/api/character/DeBlanc')
        self.assertEqual(None, res["result"][0]["real_name"][0])

    def test_character_name2(self):
        res = fetch_json('http://downing.rocks/api/character/Granny')
        self.assertEqual("Granny", res["result"][0]["name"])

    def test_team_name(self):
        res = fetch_json('http://downing.rocks/api/team/Adephi')
        self.assertEqual("Adephi", res["result"]["name"])

    def test_team_description(self):
        res = fetch_json('http://downing.rocks/api/team/Adephi')
        self.assertEqual(" ", res["result"]["description"])

    def test_team_num_appear(self):
        res = fetch_json('http://downing.rocks/api/team/Adephi')
        self.assertEqual(0, int(res["result"]["num_appearances"]))

    def test_team_image(self):
        res = fetch_json('http://downing.rocks/api/team/Adephi')
        self.assertEqual(None, res["result"]["image"])

    def test_volume_name(self):
        res = fetch_json('http://downing.rocks/api/volume/Preacher')
        self.assertEqual("Preacher", res["result"]["name"])

    def test_volume_description(self):
        res = fetch_json('http://downing.rocks/api/volume/Preacher')
        self.assertEqual("None", res["result"]["description"])

    def test_volume_num_issues(self):
        res = fetch_json('http://downing.rocks/api/volume/Preacher')
        self.assertEqual(66, int(res["result"]["num_issues"]))

    def test_invalid_URL(self):
        res = fetch_json('http://downing.rocks/api')
        self.assertEqual(None, res)

if __name__ == "__main__":
    main()

'''
...............
----------------------------------------------------------------------
Ran 15 tests in 1.733s

OK
'''