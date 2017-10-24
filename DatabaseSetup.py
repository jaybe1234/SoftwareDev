import sys
from sqlalchemy import Column , ForeignKey , Integer , String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy	 import create_engine,Float

Base = declarative_base()

#Lecturer Table
class Lecturer(Base):
    __tablename__ = 'lecturer'
    #try change lecturer id to string
    id = Column(String(20), primary_key = True)
    user_lecturer = Column(String(40),nullable = False)
    password_lecturer = Column(String(40),nullable = False)
    name_lecturer = Column(String(40),nullable = False)

#Student Table
class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer,primary_key = True,nullable=False)
    user_student = Column(String(40),nullable = False)
    password_student = Column(String(40),nullable = False)
    name_student = Column(String(40),nullable = False)
    year_student = Column(Integer,nullable = False)
    section_student = Column(String(1),nullable = False)
    gpax_student = Column(Float,nullable = False)

class Subject(Base):
    __tablename__ = 'subject'
    name_subject = Column(String(40),nullable = False)
    code_subject = Column(String(40),nullable = False,primary_key=True)

class Enrollment(Base):
    __tablename__ = 'enrollment'
    id_enrollment = Column(Integer,primary_key=True)
    student_id_enrollment = Column(Integer,nullable=True)
    lecturer_id_enrollment = Column(Integer,nullable=True)
    code_subject_enrollment= Column(String(20),ForeignKey('subject.code_subject'))
    subject_enrollment = relationship(Subject)



engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)