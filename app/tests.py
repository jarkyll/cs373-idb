from flask_testing import TestCase
from myapp import create_app, db
import unittest
# from OurModel import Character, Publisher, Volume, Team
import flask_testing

class MyTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "postgres://"
    TESTING = True
    
    def create_app(self):
        return create_app(self)

    def setUp(self):
        # db.drop_all()
        db.create_all()
        character = Character(1, 'cha', 'Austin')
        publisher = Publisher(2, 'pub', 'Houston')
        volume = Volume(3, 'sfdfdkk.jpg', 'description')
        team = Team(4, 'team', 'publisher')
        db.session.add(character)
        db.session.add(publisher)
        db.session.add(volume)
        db.session.add(team)
        db.session.commit()

    def test_Character1(self, character):
        self.assertEqual(character.id, 1)

    def test_Character2(self, character):
        self.assertEqual(character.name, 'cha')

    def test_Character3(self, character):
        self.assertEqual(character.birth, 'Austin')

    def test_Publisher1(self, publisher):
        self.assertEqual(publisher.id, 2)

    def test_Publisher2(self, publisher):
        self.assertEqual(publisher.name, 'pub')

    def test_Publisher3(self, publisher):
        self.assertEqual(publisher.locAd, 'Houston')

    def test_Volume1(self, volume):
        self.assertEqual(volume.id, 3)

    def test_Volume2(self, volume):
        self.assertEqual(volume.image, 'sfdfdkk.jpg')

    def test_Volume3(self, volume):
        self.assertEqual(volume.description, 'description')

    def test_Team1(self, team):
        self.assertEqual(team.id, 4)

    def test_Team2(self, team):
        self.assertEqual(team.name, 'team')

    def test_Team3(self, team):
        self.assertEqual(team.publisher, 'publisher')

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

    def test_Publisher_setup1(self):
        pub_test_1 = Publisher()
        db.session.add(pub_test_1)
        db.session.commit()

    def test_Publisher_setup2(self):
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

    def test_Team_setup1(self):
    	team_test1 = Team()
    	db.session.add(Team_test1)
    	db.session.commit()

    def test_Team_setup2(self):
    	team_test2 = Team()
    	db.session.add(Team_test2)
    	db.session.commit()

    def test_Team_setup3(self):
    	team_test3 = Team()
    	db.session.add(Team_test3)
    	db.session.commit()

    def test_Query1(self):
    	t = Volume()
    	db.session.add(t)
    	q = db.query.filter_by(volume=0).first(); 
    	assertEqual(t.publisher, "");

    def test_Query2(self):
        t = Publisher()
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