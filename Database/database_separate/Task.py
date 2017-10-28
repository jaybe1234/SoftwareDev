from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DatabaseSetup import Base,Grouping,Task
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
def create_task(grouping_id,task_id,name,weight):
    grouping_id = session.query(Grouping).filter_by(id_grouping=grouping_id)[0]
    new_task = Task(id_task = task_id ,name_task = name, weight_task = weight ,grouping_task = grouping_id)
    session.add(new_task)
    session.commit()
    return
def delete_task(grouping_id,task_id):
    grouping_id = session.query(Grouping).filter_by(id_grouping = grouping_id)
    task = session.query(Task).filter_by(id_task = task_id,grouping_id_task = grouping_id)[0]
    session.delete(task)
    session.commit()
    return