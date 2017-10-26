from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject,Grouping,Group,Task,Score
#from and NameOfPythonFile
engine = create_engine('sqlite:///database/database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def getStudentList(subjectCode):
    enrollList = session.query(Enrollment).filter_by(subject_code_enrollment = subjectCode)
    studentIdList = []
    studentList =[]
    for i in enrollList:
        if i.student_id_enrollment is not None:
            studentIdList.append(i.student_id_enrollment)
    for i in studentIdList:
        student = session.query(Student).filter_by(id_student = i).one()
        studentList.append(student)
    return studentList