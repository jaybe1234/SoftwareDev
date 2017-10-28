from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DatabaseSetup import Base,Task,Score
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
def create_score(task_id,student_id,score):
    task_id = session.query(Task).filter_by(id_task=task_id)[0]
    new_score = Score(score_score = score,student_id_score = student_id,task_score = task_id)
    session.add(new_score)
    session.commit()
    return
def delete_score(task_id,student_id):
    task_id = session.query(Task).filter_by(id_task = task_id)[0]
    score = session.query(Score).filter_by(task_score = task_id,student_id_score = student_id)[0]
    session.delete(score)
    session.commit()
    return