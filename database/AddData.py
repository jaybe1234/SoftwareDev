from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject,Grouping,Group,Task,Score
#from and NameOfPythonFile
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def create_student(id,user,password,name,year,section,gpax):
    new_student = Student(id_student = id, user_student = user, password_student = password, name_student =  name,year_student = year, section_student = section , gpax_student = gpax)
    session.add(new_student)
    session.commit()
    return
create_student(59340500060,'odiosaser','12345','Supitcha',2,'B',4)
create_student(59340500005,'justinunited','12345','Kanut',2,'A',4)
create_student(59340500047,'Herokids','12345','Phusana',2,'B',1)

def create_lecturer(id,user,password,name):
    new_lecturer = Lecturer(id_lecturer = id, user_lecturer = user, password_lecturer = password, name_lecturer =  name)
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

def create_enrollment(subject_code, student_id ,lecturer_id ):
    subject_code = session.query(Subject).filter_by(code_subject= subject_code)[0]
    new_enrollment = Enrollment(subject_enrollment = subject_code , student_id_enrollment = student_id,lecturer_id_enrollment = lecturer_id)
    session.add(new_enrollment)
    session.commit()
    return
create_enrollment("FRA241", 59340500060 , 1)
create_enrollment("FRA241", 59340500047 , None)
create_enrollment("FRA142", 59340500005 , None)
create_enrollment("FRA222", None , 1)
# def read_lecturer():
#     lecturers = session.query(Lecturer).all()
#     for lecturer in lecturers:#         print (lecturer.name_lecturer)
#     return

def create_grouping(grouping_id ,grouping_name,grouping_type,subject_code):
    new_grouping = Grouping(id_grouping=grouping_id,name_grouping=grouping_name,type_grouping=grouping_type,subject_code_grouping=subject_code)
    session.add(new_grouping)
    session.commit()
    return
create_grouping(1,'Grouping by GPAX','GPAX','FRA241')

def create_group(grouping_id,student_id,group_id):
    grouping_id = session.query(Grouping).filter_by(id_grouping=grouping_id)[0]
    new_group = Group(student_id_group = student_id ,group_id_group = group_id,grouping_group = grouping_id)
    session.add(new_group)
    session.commit()
    return
create_group(1,59340500060,'B01')

def create_task(grouping_id,task_id,weight):
    grouping_id = session.query(Grouping).filter_by(id_grouping=grouping_id)[0]
    new_task = Task(id_task = task_id , weight_task = weight ,grouping_task = grouping_id)
    session.add(new_task)
    session.commit()
    return
create_task(1,'Lab1',5)

def create_score(task_id,student_id,score):
    task_id = session.query(Task).filter_by(id_task=task_id)[0]
    new_score = Score(score_score = score,student_id_score = student_id,task_score = task_id)
    session.add(new_score)
    session.commit()
    return
create_score('Lab1',59340500060,99.9)


