import json
from unittest import main, TestCase
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *

class MyTests(TestCase):



    def test_artist_id(self):
        a = Publisher.query.filter_by(name='Image').first()
        self.assertEqual('Image', a.name)
        #print("Artist Test 1\nExpected: Chon\nActual: "+artist['name'])

    def test_artist_id(self):

if __name__ == "__main__":
    main()