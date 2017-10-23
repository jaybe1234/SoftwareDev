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
    id = Column(Integer,primary_key = True,nullable=False)
    user_student = Column(String(40),nullable = False)
    password_student = Column(String(40),nullable = False)
    name_student = Column(String(40),nullable = False)
    year_student = Column(Integer,nullable = False)
    section_student = Column(String(1),nullable = False)
    gpax_student = Column(Float,nullable = False)


#Subject Table
class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer,primary_key = True)
    name = Column(String(40),nullable = False)
    code = Column(String(40),nullable = False)
    enrollment = relationship('Enrollment')



engine = create_engine('sqlite:///main.db')
Base.metadata.create_all(engine)
