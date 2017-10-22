from sqlalchemy import create_engine , Float
from sqlalchemy.orm import sessionmaker
from nutty_database_setup import Base , Lecturer
engine = create_engine('sqlite:///lecturer.db')
Base.metadata.create_all(engine)
DBsession = sessionmaker(bind = engine)
session = DBsession()

def create_lecturer(user,password,name):
    new_user = Lecturer(user_lecturer = user,password_lecturer = password,name_lecturer = name)
    sesstion.add(new_user)
    sesstion.commit()
