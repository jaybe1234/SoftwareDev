from database.database_setup import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker


def connect(databasefile):
    engine = create_engine('sqlite:///' + databasefile + '.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session
