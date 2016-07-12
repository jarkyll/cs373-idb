import json
from unittest import main, TestCase
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *

class MyTests(TestCase):



    def test_publisher_name(self):
        a = Publisher.query.filter_by(name='Image').first()
        self.assertEqual('Image', a.name)

    def test_publisher_image(self):


    def test_publisher_city(self):

    def test_publisher_volume(self):

    def test_publisher_characters(self):


    def test_publisher_teams(self):


    def test_character_name(self):


    def test_character_publisher(self):


    def test_character_volumes(self):


    def test_character_teams(self):


    def test_character_image(self):


    def test_team_characters(self):


    def test_team_publisher(self):

    def test_team_volumes(self):


    def test_team_name(self):

    def test_team_image(self):

    def test_volume_name(self):

    def test_volume_publisher(self):

    def test_volume_image(self):

    def test_volume_start_year(self):

if __name__ == "__main__":
    main()