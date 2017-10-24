from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject
#from and NameOfPythonFile
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def create_student(id,user,password,name,year,section,gpax):
    new_student = Student(id = id, user_student = user, password_student = password, name_student =  name,year_student = year, section_student = section , gpax_student = gpax)
    session.add(new_student)
    session.commit()
    return
create_student(59340500060,'odiosaser','12345','Supitcha',2,'B',4)
create_student(59340500005,'justinunited','12345','Kanut',2,'A',4)
create_student(59340500047,'Herokids','12345','Phusana',2,'B',1)

def create_lecturer(id,user,password,name):
    new_lecturer = Lecturer(id = id, user_lecturer = user, password_lecturer = password, name_lecturer =  name)
    session.add(new_lecturer)
    session.commit()
    return
create_lecturer(1,"Pitiwut","12345","Mr.Pitiwut")
create_lecturer(3,"Warasinee","12345","Mrs.Warasinee")
create_lecturer(2,"Bawornsak","12345","Mr.Bawornsak")
create_lecturer(4,"Suriya","12345","Mr.Suriya")

def create_subject(name,code):
    new_subject = Subject(name_subject = name , code_subject = code)
    session.add(new_subject)
    session.commit()
    return
create_subject('Software Development','FRA241')
create_subject('Computer Programming','FRA142')
create_subject('Digital','FRA221')
create_subject('Sensor&Actuator','FRA222')

def create_enrollment(id,code, student_id ,lecturer_id ):
    new_enrollment = Enrollment(id_enrollment = id , subject_enrollment = code , student_id_enrollment = student_id,lecturer_id_enrollment = lecturer_id)
    session.add(new_enrollment)
    session.commit()
    return
#create_enrollment()

#cannot specific subject
def read_subject():
    subjects = session.query(Subject).all()
    for subject in subjects:
        result = subject
    return result
print (read_subject())
create_enrollment(1,read_subject(), 59340500060 , None)
create_enrollment(2,read_subject(), 59340500047 , None)
create_enrollment(3,read_subject(), 59340500005 , None)
create_enrollment(4,read_subject(), None , 1)
# def read_lecturer():
#     lecturers = session.query(Lecturer).all()
#     for lecturer in lecturers:#         print (lecturer.name_lecturer)
#     return
