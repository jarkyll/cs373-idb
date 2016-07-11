from app import app, db
from app.models import *
import os, glob
import json
from pprint import pprint


PublisherName = ['Aftershock Comics', 'Boom! Studios', 'Dark Horse Comics', 'Dell', 'Fiction House', 'IDW Publishing', 'Image', 'Top Cow', 'Valiant', 'Vertigo']

dir = os.getcwd() + '/'
def add_publishers():
    db.create_all()
    for publisher in PublisherName:
        f = open( dir + 'database/publishers/' + publisher + '/' + publisher + '.json', 'r')
        test = json.load(f)
        pprint(test.keys())
        if test['deck'] is None:
            test['deck'] = ''
        pub = {
            'name': test['name'],
            'address': test['location']['address'],
            'city': test['location']['city'],
            'state': test['location']['state'],
            'deck': test['deck'],
            'image': test['image']
        }

        pub = Publisher(**pub)
        try:
            db.session.add(pub)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
    '''
    pub = (**DEMO)

    try:
        db.session.add(pub)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
    '''




if __name__ == '__main__':
    add_publishers()
    app.run()
