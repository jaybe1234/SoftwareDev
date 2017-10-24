from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database_setup import Base, Lecturer
from database.create_subject_database import Enrollment
engine = create_engine('sqlite:///main.db')
Base.metadata.create_all(engine)
DBsession = sessionmaker(bind = engine)
session = DBsession()

def create_lecturer(numid,user,password,name):
    new_user = Lecturer(id = numid,user_lecturer = user,password_lectuer = password, name_lecturer = name)
    session.add(new_user)
    session.commit()

create_lecturer(1, 'Blink', 'Bawornsak', 'eiei')