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
    id_lecturer = Column(Integer, primary_key = True)
    user_lecturer = Column(String(20),nullable = False)
    password_lecturer = Column(String(20),nullable = False)
    name_lecturer = Column(String(20),nullable = False)

#Student Table
class Student(Base):
    __tablename__ = 'student'
    id_student = Column(Integer,primary_key = True,nullable=False)
    user_student = Column(String(20),nullable = False)
    password_student = Column(String(20),nullable = False)
    name_student = Column(String(20),nullable = False)
    year_student = Column(Integer,nullable = False)
    section_student = Column(String(1),nullable = False)
    gpax_student = Column(Float,nullable = False)
    # email_student = Column(String(50),nullable = False)

class Subject(Base):
    __tablename__ = 'subject'
    name_subject = Column(String(20),nullable = False)
    code_subject = Column(String(20),nullable = False,primary_key=True)

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
    id_grouping = Column(Integer,nullable=True,primary_key=True)
    name_grouping = Column(String(20),nullable=False)
    type_grouping = Column(String(20),nullable=False)
    # subject_code_grouping = Column(String(40),nullable=False)
    subject_code_grouping = Column(String(20),ForeignKey('subject.code_subject'))
    subject_grouping = relationship(Subject)

class Group(Base):
    __tablename__ = 'group'
    primary_key = Column(Integer,nullable=True,primary_key=True)
    student_id_group = Column(Integer,nullable=False)
    group_id_group = Column(String(20),nullable=False)
    grouping_id_group = Column(Integer,ForeignKey('grouping.id_grouping'))
    grouping_group = relationship(Grouping)

class Task(Base):
    __tablename__ = 'task'
    id_task = Column(Integer,nullable=True,primary_key=True)
    name_task = Column(String(30),nullable =False)
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

class Credit(Base):
    __tablename__ = 'credit'
    group_id_credit = Column(String(20),nullable=False,primary_key=True)
    grouping_id_credit = Column(Integer,nullable=False)
    credit = Column(Float,nullable=False)
    # credit bug : add more column that is task name
    task_name_credit = Column(String(20),nullable=False)

class Archive(Base):
    __tablename__ = 'archive'
    primary_key = Column(Integer,nullable=True,primary_key = True)
    lecturer_id_archive = Column(Integer,ForeignKey('lecturer.id_lecturer'))
    subject_code_archive = Column(String(20),nullable=False)
    lecturer_archive = relationship(Lecturer)

class Storage(Base):
    __tablename__ = 'storage'
    primary_key = Column(Integer,nullable=True,primary_key = True)
    student_id_storage = Column(Integer,nullable=False)
    task_name_storage = Column(String(30),nullable=False)
    score_storage = Column(Integer,nullable=False)


engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
