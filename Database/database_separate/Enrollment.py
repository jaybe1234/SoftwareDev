from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.DatabaseSetup import Base,Enrollment,Subject,Grouping,Group,Task,Score
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
def create_enrollment(subject_code, student_id ,lecturer_id ):
    subject_code = session.query(Subject).filter_by(code_subject= subject_code)[0]
    new_enrollment = Enrollment(subject_enrollment = subject_code , student_id_enrollment = student_id,lecturer_id_enrollment = lecturer_id)
    session.add(new_enrollment)
    session.commit()
    return
#delete student in specific subject
def delete_student_enrollment(student_id,subject_code):
    subject_code = session.query(Subject).filter_by(code_subject = subject_code)[0]
    student = session.query(Enrollment).filter_by(student_id_enrollment = student_id,subject_enrollment = subject_code)[0]
    enrollment_grouping = session.query(Grouping).filter_by(subject_grouping = subject_code)[0]
    enrollment_group = session.query(Group).filter_by(grouping_group = enrollment_grouping,student_id_group = student_id)[0]
    enrollment_task = session.query(Task).filter_by(grouping_task = enrollment_grouping)[0]
    enrollment_score = session.query(Score).filter_by(task_score = enrollment_task,student_id_score = student_id)[0]
    session.delete(enrollment_score)
    session.delete(enrollment_group)
    session.delete(student)
    session.commit()
    return
#delete lecturer in specific subject
def delete_lecturer_enrollment(lecturer_id,subject_code):
    lecturer = session.query(Enrollment).filter_by(lecturer_id_enrollment = lecturer_id,subject_code_enrollment = subject_code)[0]
    session.delete(lecturer)
    session.commit()
    return