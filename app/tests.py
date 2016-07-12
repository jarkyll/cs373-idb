from unittest import main, TestCase

from models import *


class MyTests(TestCase):



    def test_publisher_name(self):
        a = Publisher.query.filter_by(name='Image').one()
        self.assertEqual('Image', a.name)

    def test_publisher_image(self):
        a = Publisher.query.filter_by(name='Image').one()
        self.assertEqual('http://static4.comicvine.com/uploads/scale_small/14/148518/2973722-hackslashdollar.jpg?api_key=d1fcd2dc19ac4cbac24fd26d5161210b150cbaed&format=json', a.image)

    def test_publisher_city(self):
        pub = Publisher.query.filter_by(name='Vertigo').one()
        self.assertEqual('New York City', pub.city)

    def test_publisher_volume(self):
        pub = Publisher.query.filter_by(name='Vertigo').one()
        self.assertEqual(15, len(pub.publisher_volumes))

    def test_publisher_characters(self):
        pub = Publisher.query.filter_by(name='Vertigo').one()
        self.assertEqual(41, len(pub.publisher_characters))

    def test_publisher_teams(self):
        pub = Publisher.query.filter_by(name='Vertigo').one()
        self.assertEqual(10, len(pub.publisher_teams))

    def test_character_name(self):
        char = Character.query.filter_by(name='Jerry').one()
        self.assertEqual('Jerry', char.name)

    def test_character_publisher(self):
        char = Character.query.filter_by(name='Jerry').one()
        self.assertEqual('Dell', char.character_publisher.name)

    def test_character_volumes(self):
        char = Character.query.filter_by(name='Jerry').one()
        self.assertEqual(2, len(char.character_volumes))

    def test_character_teams(self):
        char = Character.query.filter_by(name='Jerry').one()
        self.assertEqual(1, len(char.character_teams))

    def test_character_image(self):
        char = Character.query.filter_by(name='Jerry').one()
        self.assertEqual('http://comicvine.gamespot.com/api/image/scale_small/277673-175026-jerry.jpg', char.image)

    def test_team_characters(self):
        team = Team.query.filter_by(name='Ewoks').one()
        self.assertEqual(5, len(team.team_characters))

    def test_team_publisher(self):
        team = Team.query.filter_by(name='Ewoks').one()
        self.assertEqual(5, len(team.team_characters))
    def test_team_volumes(self):
        team = Team.query.filter_by(name='Ewoks').one()
        self.assertEqual(5, len(team.team_characters))

    def test_team_name(self):
        team = Team.query.filter_by(name='Ewoks').one()
        self.assertEqual(5, len(team.team_characters))

    def test_team_image(self):
        team = Team.query.filter_by(name='Ewoks').one()
        self.assertEqual('http://comicvine.gamespot.com/api/image/scale_small/367187-154544-ewoks.JPG', team.image)

    def test_volume_name(self):
        vol = Volume.query.filter_by(name='The Sandman').one()
        self.assertEqual('The Sandman', vol.name)

    def test_volume_publisher(self):
        vol = Volume.query.filter_by(name='The Sandman').one()
        self.assertEqual('Vertigo', vol.publisher_name)

    def test_volume_image(self):
        vol = Volume.query.filter_by(name='The Sandman').one()
        self.assertEqual('http://comicvine.gamespot.com/api/image/scale_small/2199272-01.jpg', vol.image)

    def test_volume_start_year(self):
        vol = Volume.query.filter_by(name='The Sandman').one()
        self.assertEqual(1989, vol.start_year)

if __name__ == "__main__":
    main()