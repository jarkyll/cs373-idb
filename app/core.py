from app.models import Volume
from app import db


def create_db():
    db.create_all()
    db.session.commit()

    DEMO = {
    'name': "tesing"
    }

    pub = Volume(**DEMO)

    try:
        db.session.add(pub)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
