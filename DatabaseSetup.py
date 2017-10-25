import sys
from sqlalchemy import Column , ForeignKey , Integer , String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy	 import create_engine,Float

Base = declarative_base()

"""
#################### READ THIS #######################
It may have change some code
"""""

#Lecturer Table
class Lecturer(Base):
    __tablename__ = 'lecturer'
    #try change lecturer id to string
    id_lecturer = Column(String(20), primary_key = True)
    user_lecturer = Column(String(40),nullable = False)
    password_lecturer = Column(String(40),nullable = False)
    name_lecturer = Column(String(40),nullable = False)

#Student Table
class Student(Base):
    __tablename__ = 'student'
    id_student = Column(Integer,primary_key = True,nullable=False)
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
    primary_key = Column(Integer,nullable=True,primary_key=True)
    student_id_enrollment = Column(Integer,nullable=True)
    lecturer_id_enrollment = Column(Integer,nullable=True)
    subject_code_enrollment= Column(String(20),ForeignKey('subject.code_subject'))
    subject_enrollment = relationship(Subject)

#Not yet relationship between Grouping and Enrollment

class Grouping(Base):
    __tablename__ = 'grouping'
    primary_key = Column(Integer,nullable=True,primary_key=True)
    id_grouping = Column(Integer,nullable=False)
    name_grouping = Column(String(40),nullable=False)
    type_grouping = Column(String(40),nullable=False)
    subject_code_grouping = Column(String(40),nullable=False)

class Group(Base):
    __tablename__ = 'group'
    primary_key = Column(Integer,nullable=True,primary_key=True)
    student_id_group = Column(Integer,nullable=False)
    group_id_group = Column(String(20),nullable=False)
    grouping_id_group = Column(Integer,ForeignKey('grouping.id_grouping'))
    grouping_group = relationship(Grouping)

class Task(Base):
    __tablename__ = 'task'
    primary_key = Column(Integer,nullable=True,primary_key=True)
    id_task = Column(String(20),nullable=False)
    weight_task = Column(Float,nullable=False)
    grouping_id_task = Column(Integer,ForeignKey('grouping.id_grouping'))
    grouping_task = relationship(Grouping)

class Score(Base):
    __tablename__ = 'score'
    primary_key = Column(Integer,nullable=True,primary_key = True)
    score_score = Column(Float,nullable=False)
    student_id_score = Column(Integer,nullable=False)
    task_id_score = Column(String(20),ForeignKey('task.id_task'))
    task_score = relationship(Task)

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)