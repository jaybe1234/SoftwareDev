import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationships
from sqlalchemy import create_engine
Base = declarative_base()

#Student Table
class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, nullable=False, primary_key= True)
    name = Column(String(250), nullable=False)
    user = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    year = Column(Integer)
    section = Column(Integer, nullable=False)
    gpax = Column(Float, nullable= False)

#Lecturer Table
class Lecturer(Base):
    __tablename__ = 'lecturer'
    id = Column(Integer, nullable= False, primary_key= True)
    name = Column(String(250), nullable= False)
    user = Column(String(250), nullable= False)
    password = Column(String(250), nullable= False)

#Subject
class Subject(Base):
    __tablename__ = 'subject'
    code = Column(String(250), nullable= False, primary_key= True)
    name = Column(String(250, nullable = False))


engine = create_engine('sqlite:///GradingSystem.db')
Base.metadata.create_all(engine)