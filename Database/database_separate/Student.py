from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DatabaseSetup import Base,Student,Enrollment,Grouping,Group,Task,Score
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
def create_student(id,user,password,name,year,section,gpax):
    new_student = Student(id_student = id, user_student = user, password_student = password, name_student =  name,year_student = year, section_student = section , gpax_student = gpax)
    session.add(new_student)
    session.commit()
    return
def delete_student(id):
    student = session.query(Student).filter_by(id_student = id)[0]
    student_enrollment = session.query(Enrollment).filter_by(student_id_enrollment = id)
    for enrollment in student_enrollment:
        student_grouping = session.query(Grouping).filter_by(subject_grouping = enrollment.subject_enrollment)
        for grouping in student_grouping:
            student_group = session.query(Group).filter_by(grouping_group =grouping,student_id_group =id)
            for group in student_group:
                session.delete(group)
            student_task = session.query(Task).filter_by(task_score = grouping)
            for task in student_task:
                student_score = session.query(Score).filter_by(task_score = task,student_id_score = id)
                for score in student_score:
                    session.delete(score)
        session.delete(enrollment)
    session.delete(student)
    session.commit()
    return

