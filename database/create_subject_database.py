import sys
from sqlalchemy import Column , ForeignKey , Integer , String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy	 import create_engine,Float
from database.database_setup import Lecturer, Student, Subject, Base
import sqlite3



# Enrollment Table
class Enrollment(Base):
    __tablename__ = 'enrollment'
    id = Column(Integer, primary_key=True)
    student_id = Column(String(40), ForeignKey(Student.id))
    lecturer_id = Column(String(40), ForeignKey(Lecturer.id))
    subject = Column(String(40), ForeignKey(Subject.code))


# Score Table
class Score(Base):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True)
    score = Column(Integer, nullable=False)


# Task Table
class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    weight = Column(Float, nullable=False)
    description = Column(String(40), nullable=False)
    fullscore_task = Column(Integer, nullable=False)


# Grouping Table
class Grouping(Base):
    __tablename__ = 'grouping'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    typegroup = Column(String(40), nullable=False)

def create_subject_database(subjectname):
    engine = create_engine('sqlite:///'+ subjectname +'.db')
    Base.metadata.create_all(engine)

def add_column(database_name, table_name, column_name, data_type):

  connection = sqlite3.connect(database_name)
  cursor = connection.cursor()

  if data_type == "Integer":
    data_type_formatted = "INTEGER"


  elif data_type == "String":
    data_type_formatted = "VARCHAR(100)"

  elif data_type == "Float":
      data_type_formatted = "FLOAT"


  format_str = ("ALTER TABLE '{table_name}' ADD column '{column_name}' '{data_type}'")
  sql_command = format_str.format(table_name=table_name, column_name=column_name, data_type=data_type_formatted)

  cursor.execute(sql_command)
  connection.commit()
  connection.close()


