from sqlalchemy import create_engine , Float
from sqlalchemy.orm import sessionmaker
from nutty_database_setup import Base , Task
engine = create_engine('sqlite:///task.db')
Base.metadata.create_all(engine)
DBsession = sessionmaker(bind = engine)
session = DBsession()

def create_task(weight,des,fscore):
    new_task = Task(weight = weight,description = des,fullscore_task = int(fscore))
    session.add(new_task)
    session.commit()
