from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.DatabaseSetup import Base,Grouping,Group,Task,Score
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
def create_grouping(grouping_id ,grouping_name,grouping_type,subject_code):
    new_grouping = Grouping(id_grouping=grouping_id,name_grouping=grouping_name,type_grouping=grouping_type,subject_code_grouping=subject_code)
    session.add(new_grouping)
    session.commit()
    return
def delete_grouping(grouping_id):
    grouping = session.query(Grouping).filter_by(id_grouping = grouping_id)[0]
    grouping_group = session.query(Group).filter_by(grouping_group = grouping)
    grouping_task = session.query(Task).filter_by(grouping_task = grouping)
    for sometask in grouping_task:
        grouping_score = session.query(Score).filter_by(task_score = sometask)
        for somescore in grouping_score:
            session.delete(somescore)
        session.delete(sometask)
    for somegroup in grouping_group:
        session.delete(somegroup)
    session.delete(grouping)
    session.commit()
    return