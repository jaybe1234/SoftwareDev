from sqlalchemy import create_engine , Float
from sqlalchemy.orm import sessionmaker
from nutty_database_setup import Base , Student
engine = create_engine('sqlite:///student.db')
Base.metadata.create_all(engine)
DBsession = sessionmaker(bind = engine)
session = DBsession()

def create_student(numid,user,password,name,year,sec,gpax):
    new_user = Student(id_student = numid,name_student = name,user_student = user,password_student = password, year_student = int(year) , section_student = sec , gpax_student  = Float(gpax))
    sesstion.add(new_user)
    sesstion.commit()
