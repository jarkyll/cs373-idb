from flask_testing import TestCase
from myapp import create_app, db
import unittest
//from OurModel import Character, Publisher, Volume, Series
import flask_testing

class MyTest(TestCase):
	SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        # pass in test configuration
        return create_app(self)

    def setUp(self):
    	db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_Character_setup1(self):
    	character_test = Character()
    	db.session.add(character_test)
    	db.session.commit()

    def test_Character_setup2(self):
    	character_test2 = Character()
    	db.session.add(character_test2)
    	db.session.commit()

    def test_Character_setup3(self):
    	character_test3 = Character()
    	db.session.add(character_test3)
    	db.session.commit()

    def test_publisher_setup1(self):
        pub_test_1 = Publisher()
        db.session.add(pub_test_1)
        db.session.commit()

    def test_publisher_setup2(self):
        data_test_2 = Publisher()
        db.session.add(data_test_2)
        db.session.commit()

    def test_Publisher_setup3(self):
        data_test_3 = Publisher()
        db.session.add(data_test_3)
        db.session.commit()

    def test_Volume_setup1(self):
    	volume_test1 = Volume()
    	db.session.add(volume_test1)
    	db.session.commit()

    def test_Volume_setup2(self):
    	volume_test2 = Volume()
    	db.session.add(volume_test2)
    	db.session.commit()

    def test_Volume_setup3(self):
    	volume_test3 = Volume()
    	db.session.add(volume_test3)
    	db.session.commit()

    def test_Series_setup1(self):
    	series_test1 = Series()
    	db.session.add(series_test1)
    	db.session.commit()

    def test_Series_setup2(self):
    	series_test2 = Series()
    	db.session.add(series_test2)
    	db.session.commit()

    def test_Series_setup3(self):
    	series_test3 = Series()
    	db.session.add(series_test3)
    	db.session.commit()

    def test_Query1(self):
    	t = Volume()
    	db.session.add(t)
    	q = db.query.filter_by(volume=0).first(); 
    	assertEqual(t.publisher, "");


	def test_Query2(self):
    	t = Series()
    	db.session.add(t)
    	q = db.query.filter_by(publisher="").first(); 
    	assertEqual(t.publisher, "");    

    def test_Query3(self):
    	t = Volume()
    	db.session.add(t)
    	q = db.query.filter_by(volume=0).all(); 
    	assertEqual(q.size(), 0);

# your test cases

if __name__ == '__main__':
    unittest.main()