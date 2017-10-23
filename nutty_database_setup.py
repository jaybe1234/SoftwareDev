import sys
from sqlalchemy import Column , ForeignKey , Integer , String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy	 import create_engine,Float

Base = declarative_base()

#Lecturer Table
class Lecturer(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    user_lecturer = Column(String(40),nullable = False)
    password_lecturer = Column(String(40),nullable = False)
    name_lecturer = Column(String(40),nullable = False)

#Student Table
class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer,primary_key = True)
    id_student = Column(String(40),nullable = False)
    user_student = Column(String(40),nullable = False)
    password_student = Column(String(40),nullable = False)
    name_student = Column(String(40),nullable = False)
    year_student = Column(Integer,nullable = False)
    section_student = Column(String(1),nullable = False)
    gpax_student = Column(Float,nullable = False)

#Enrollment Table
class Enrollment(Base):
    __tablename__ = 'enrollment'
    id = Column(Integer,primary_key = True)
    student_id = Column(String(40),ForeignKey(Student.id))
    lecturer_id = Column(String(40),ForeignKey(Lecturer.id))
    subject = Column(String(40), ForeignKey(Subject.code))

#Score Table
class Score(Base):
    __tablename__ = 'score'
    id = Column(Integer,primary_key = True)
    task = Column(Integer,ForeignKey(Task.id))
    score = Column(Integer,nullable = False)

#Task Table
class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer,primary_key = True)
    weight = Column(Float,nullable = False)
    description = Column(String(40),nullable = False)
    fullscore_task = Column(Integer,nullable = False)

#Subject Table
class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer,primary_key = True)
    name = Column(String(40),nullable = False)
    code = Column(String(40),nullable = False)
    enrollment = relationship(Enrollment)


#Grouping Table
class Grouping(Base):
    __tablename__ = 'grouping'
    id = Column(Integer,primary_key = True)
    name = Column(String(40),nullable = False)
    typegroup = Column(String(40),nullable = False)





engine = create_engine('sqlite:///all.db')
Base.metadata.create_all(engine)
