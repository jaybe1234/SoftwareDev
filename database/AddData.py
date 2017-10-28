from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject,Grouping,Group,Task,Score
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def create_student(id,user,password,name,year,section,gpax):
    new_student = Student(id_student = id, user_student = user, password_student = password, name_student =  name,year_student = year, section_student = section , gpax_student = gpax)
    session.add(new_student)
    session.commit()
    return
def delete_student(id):
    student = session.query(Student).filter_by(id_student = id)[0]
    student_enrollment = session.query(Enrollment).filter_by(student_id_enrollment = id)
    for enrollment in student_enrollment:
        student_grouping = session.query(Grouping).filter_by(subject_grouping = enrollment.subject_enrollment)
        for grouping in student_grouping:
            student_group = session.query(Group).filter_by(grouping_group =grouping,student_id_group =id)
            for group in student_group:
                session.delete(group)
            student_task = session.query(Task).filter_by(task_score = grouping)
            for task in student_task:
                student_score = session.query(Score).filter_by(task_score = task,student_id_score = id)
                for score in student_score:
                    session.delete(score)
        session.delete(enrollment)
    session.delete(student)
    session.commit()
    return
######################################################################################
def create_lecturer(id,user,password,name):
    new_lecturer = Lecturer(id_lecturer = id, user_lecturer = user, password_lecturer = password, name_lecturer =  name)
    session.add(new_lecturer)
    session.commit()
    return
def delete_lecturer(id):
    old_lecturer = session.query(Lecturer).filter_by(id_lecturer=id)[0]
    session.delete(old_lecturer)
    old_lecturer_enrollment = session.query(Enrollment).filter_by(lecturer_id_enrollment = id)
    for someone in old_lecturer_enrollment:
        session.delete(someone)
    session.commit()
    return
######################################################################################
def create_subject(name,code):
    new_subject = Subject(name_subject = name , code_subject = code)
    session.add(new_subject)
    session.commit()
    return
def delete_subject(subject_code):
    subject_code = session.query(Subject).filter_by(code_subject = subject_code)[0]
    subject_enrollment = session.query(Enrollment).filter_by(subject_enrollment = subject_code)
    subject_grouping = session.query(Grouping).filter_by(subject_grouping = subject_code)
    for grouping in subject_grouping:
        subject_group =session.query(Group).filter_by(grouping_group = grouping)
        for group in subject_group:
            session.delete(group)
        subject_task = session.query(Task).filter_by(grouping_task = grouping)
        for task in subject_task:
            subject_score = session.query(Score).filter_by(task_score = task)
            for score in subject_score:
                session.delete(score)
            session.delete(task)
        session.delete(grouping)
    for enrollment in subject_enrollment:
        session.delete(enrollment)
    session.delete(subject_code)
    session.commit()
    return
######################################################################################
def create_enrollment(subject_code, student_id ,lecturer_id ):
    subject_code = session.query(Subject).filter_by(code_subject= subject_code)[0]
    new_enrollment = Enrollment(subject_enrollment = subject_code , student_id_enrollment = student_id,lecturer_id_enrollment = lecturer_id)
    session.add(new_enrollment)
    session.commit()
    return
#delete student in specific subject
def delete_student_enrollment(student_id,subject_code):
    subject_code = session.query(Subject).filter_by(code_subject = subject_code)[0]
    student = session.query(Enrollment).filter_by(student_id_enrollment = student_id,subject_enrollment = subject_code)[0]
    enrollment_grouping = session.query(Grouping).filter_by(subject_grouping = subject_code)[0]
    enrollment_group = session.query(Group).filter_by(grouping_group = enrollment_grouping,student_id_group = student_id)[0]
    enrollment_task = session.query(Task).filter_by(grouping_task = enrollment_grouping)[0]
    enrollment_score = session.query(Score).filter_by(task_score = enrollment_task,student_id_score = student_id)[0]
    session.delete(enrollment_score)
    session.delete(enrollment_group)
    session.delete(student)
    session.commit()
    return
#delete lecturer in specific subject
def delete_lecturer_enrollment(lecturer_id,subject_code):
    lecturer = session.query(Enrollment).filter_by(lecturer_id_enrollment = lecturer_id,subject_code_enrollment = subject_code)[0]
    session.delete(lecturer)
    session.commit()
    return
######################################################################################
def create_grouping(grouping_id ,grouping_name,grouping_type,subject_code):
    new_grouping = Grouping(id_grouping=grouping_id,name_grouping=grouping_name,type_grouping=grouping_type,subject_code_grouping=subject_code)
    session.add(new_grouping)
    session.commit()
    return
def delete_grouping(grouping_id):
    #change subject_code into object
    grouping = session.query(Grouping).filter_by(id_grouping = grouping_id)[0]
    grouping_group = session.query(Group).filter_by(grouping_group = grouping)
    grouping_task = session.query(Task).filter_by(grouping_task = grouping)
    for sometask in grouping_task:
        grouping_score = session.query(Score).filter_by(task_score = sometask)
        for somescore in grouping_score:
            session.delete(somescore)
        session.delete(sometask)
    for somegroup in grouping_group:
        session.delete(somegroup)
    session.delete(grouping)
    session.commit()
    return
######################################################################################
def create_group(grouping_id,student_id,group_id):
    grouping_id = session.query(Grouping).filter_by(id_grouping=grouping_id)[0]
    new_group = Group(student_id_group = student_id ,group_id_group = group_id, grouping_group = grouping_id)
    session.add(new_group)
    session.commit()
    return
#Dont have delete function in group
######################################################################################
def create_task(grouping_id,task_id,name,weight):
    grouping_id = session.query(Grouping).filter_by(id_grouping=grouping_id)[0]
    new_task = Task(id_task = task_id ,name_task = name, weight_task = weight ,grouping_task = grouping_id)
    session.add(new_task)
    session.commit()
    return
def delete_task(task_id,grouping_id):
    grouping_id = session.query(Grouping).filter_by(id_grouping = grouping_id)
    task = session.query(Task).filter_by(id_task = task_id,grouping_id_task = grouping_id)[0]
    session.delete(task)
    session.commit()
    return
######################################################################################
def create_score(task_id,student_id,score):
    task_id = session.query(Task).filter_by(id_task=task_id)[0]
    new_score = Score(score_score = score,student_id_score = student_id,task_score = task_id)
    session.add(new_score)
    session.commit()
    return
def delete_score(task_id,student_id):
    task_id = session.query(Task).filter_by(id_task = task_id)[0]
    score = session.query(Score).filter_by(task_score = task_id,student_id_score = student_id)[0]
    session.delete(score)
    session.commit()
    return
######################################################################################
"""
create_student(59340500060,'odiosaser','12345','Supitcha',2,'B',4)
create_student(59340500005,'justinunited','12345','Kanut',2,'A',4)
create_student(59340500047,'Herokids','12345','Phusana',2,'B',1)

create_lecturer(1,"Pitiwut","12345","Mr.Pitiwut")
create_lecturer(3,"Warasinee","12345","Mrs.Warasinee")
create_lecturer(2,"Bawornsak","12345","Mr.Bawornsak")
create_lecturer(4,"Suriya","12345","Mr.Suriya")

create_subject('Software Development','FRA241')
create_subject('Computer Programming','FRA142')
create_subject('Digital','FRA221')
create_subject('Sensor&Actuator','FRA222')

create_enrollment("FRA241", 59340500060 , None)
create_enrollment("FRA241", None , 1)
create_enrollment("FRA241", 59340500047 , None)
create_enrollment("FRA142", 59340500005 , None)
create_enrollment("FRA222", None , 1)

create_grouping(1,'Grouping by GPAX','GPAX','FRA241')
create_grouping(2,'Grouping by SECTION','SEC','FRA142')

create_group(1,59340500060,'B01')

create_task(1,'T001','Lab1',5)
create_task(2,'T002','Lab1',5)

create_score('T001',59340500060,99.9)"""
"""
# delete_student(59340500005)

# delete_subject('FRA241')

# delete_student_enrollment(59340500060,"FRA241")

# delete_lecturer_enrollment(1,'FRA241')

# delete_score("T001",59340500060)

# delete_task('T001',1)

# delete_grouping(1)