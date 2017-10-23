from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database_setup import Base, Subject
engine = create_engine('sqlite:///main.db')
Base.metadata.create_all(engine)
DBsession = sessionmaker(bind = engine)
session = DBsession()

def create_student(numid,name,code,en):
    new_subject = Subject(id = numid,name = name,code = code, enrollment = en)
    session.add(new_subject)
    session.commit()
