from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.DatabaseSetup import Base,Enrollment,Subject,Grouping,Group,Task,Score
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
def create_subject(name,code):
    new_subject = Subject(name_subject = name , code_subject = code)
    session.add(new_subject)
    session.commit()
    return
def delete_subject(subject_code):
    subject_code = session.query(Subject).filter_by(code_subject = subject_code)[0]
    subject_enrollment = session.query(Enrollment).filter_by(subject_enrollment = subject_code)
    subject_grouping = session.query(Grouping).filter_by(subject_grouping = subject_code)
    for grouping in subject_grouping:
        subject_group =session.query(Group).filter_by(grouping_group = grouping)
        for group in subject_group:
            session.delete(group)
        subject_task = session.query(Task).filter_by(grouping_task = grouping)
        for task in subject_task:
            subject_score = session.query(Score).filter_by(task_score = task)
            for score in subject_score:
                session.delete(score)
            session.delete(task)
        session.delete(grouping)
    for enrollment in subject_enrollment:
        session.delete(enrollment)
    session.delete(subject_code)
    session.commit()
    return