from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database_setup import Base, Lecturer, Student, Subject
engine = create_engine('sqlite:///main.db')
Base.metadata.create_all(engine)
DBsession = sessionmaker(bind = engine)
session = DBsession()

def create_lecturer(numid,user,password,name):
    new_user = Lecturer(id = numid,username = user,password = password, name = name)
    session.add(new_user)
    session.commit()


new_user = Lecturer(id=1, username='Bawornsak', password='1234', name='Blink')
session.add(new_user)
session.commit()