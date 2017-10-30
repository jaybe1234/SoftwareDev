from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from Database.DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject,Grouping,Group,Task,Score,Credit

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
def create_grouping(grouping_name,grouping_type,subject_code):
    new_grouping = Grouping(name_grouping=grouping_name,type_grouping=grouping_type,subject_code_grouping=subject_code)
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
def create_task(grouping_id,name,weight):
    grouping_id = session.query(Grouping).filter_by(id_grouping=grouping_id)[0]
    new_task = Task(name_task = name, weight_task = weight ,grouping_task = grouping_id)
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

def create_credit(group_id,subject_code,credit):
    groups = session.query(Group).filter_by(group_id_group = group_id)
    for somegroup in groups:
        if somegroup.grouping_group.subject_code_grouping == subject_code:
            new_credit = Credit(group_id_credit = group_id , grouping_id_credit = somegroup.grouping_id_group,credit = credit)
            session.add(new_credit)
            session.commit()
    return

#
# create_student(59340500001,'A','12345','AA',2,'A',4.00)
# create_student(59340500002,'B','12345','BB',2,'A',4.00)
# create_student(59340500003,'C','12345','CC',2,'A',1.52)
# create_student(59340500004,'D','12345','DD',2,'A',4.00)
# create_student(59340500005,'E','12345','EE',2,'A',4.00)
# create_student(59340500006,'F','12345','FF',2,'A',1.00)
# create_student(59340500007,'G','12345','GG',2,'A',2.73)
# create_student(59340500008,'H','12345','HH',2,'A',2.65)
# create_student(59340500009,'I','12345','II',2,'A',1.88)
# create_student(59340500010,'J','12345','JJ',2,'A',3.24)
# create_student(59340500011,'K','12345','KK',2,'B',3.55)
# create_student(59340500012,'L','12345','LL',2,'B',1.99)
# create_student(59340500013,'M','12345','MM',2,'B',4.00)
# create_student(59340500014,'N','12345','NN',2,'B',4.00)
# create_student(59340500015,'O','12345','OO',2,'B',1.54)
# create_student(59340500016,'P','12345','PP',2,'B',4.00)
# create_student(59340500017,'Q','12345','QQ',2,'B',4.00)
# create_student(59340500018,'R','12345','RR',2,'B',1.00)
# create_student(59340500019,'S','12345','SS',2,'B',3.06)
# create_student(59340500020,'T','12345','TT',2,'B',2.01)
#
#
# create_lecturer(1,"Pitiwut","12345","Mr.Pitiwut")
# create_lecturer(2,"Warasinee","12345","Mrs.Warasinee")
# create_lecturer(3,"Bawornsak","12345","Mr.Bawornsak")
# create_lecturer(4,"Suriya","12345","Mr.Suriya")
# create_lecturer(5,"Pitiwut2","12345","Mr.Pitiwut2")
# create_lecturer(6,"Warasinee2","12345","Mrs.Warasinee2")
# create_lecturer(7,"Bawornsak2","12345","Mr.Bawornsak2")
# create_lecturer(8,"Suriya2","12345","Mr.Suriya2")
#
# create_subject('Software Development','FRA241')
# create_subject('Computer Programming','FRA142')
# create_subject('Digital','FRA221')
# create_subject('Sensor&Actuator','FRA222')
# create_subject('Digital2','FRA221.2')
# create_subject('Sensor&Actuator2','FRA222.2')
#
#
# create_enrollment("FRA241", 59340500001 , None)
# create_enrollment("FRA241", 59340500002 , None)
# create_enrollment("FRA241", 59340500003 , None)
# create_enrollment("FRA241", 59340500004 , None)
# create_enrollment("FRA241", 59340500005 , None)
# create_enrollment("FRA241", 59340500006 , None)
# create_enrollment("FRA241", 59340500007 , None)
# create_enrollment("FRA241", 59340500008 , None)
# create_enrollment("FRA241", 59340500009 , None)
# create_enrollment("FRA241", 59340500010 , None)
# create_enrollment("FRA241", 59340500011 , None)
# create_enrollment("FRA241", 59340500012 , None)
# create_enrollment("FRA241", 59340500013 , None)
# create_enrollment("FRA241", 59340500014 , None)
# create_enrollment("FRA241", 59340500015 , None)
# create_enrollment("FRA241", 59340500016 , None)
# create_enrollment("FRA241", 59340500017 , None)
# create_enrollment("FRA241", 59340500018 , None)
# create_enrollment("FRA241", 59340500019 , None)
# create_enrollment("FRA241", 59340500020 , None)
#
# create_enrollment("FRA142", 593405000001 , None)
# create_enrollment("FRA142", 593405000001 , None)
# create_enrollment("FRA142", 593405000003 , None)
# create_enrollment("FRA142", 593405000004 , None)
# create_enrollment("FRA142", 593405000005 , None)
# create_enrollment("FRA142", 593405000006 , None)
# create_enrollment("FRA142", 593405000007 , None)
# create_enrollment("FRA142", 593405000008 , None)
# create_enrollment("FRA142", 593405000009 , None)
# create_enrollment("FRA142", 593405000010 , None)
#
# create_grouping('Grouping by GPAX','GPAX','FRA241')
# create_grouping('Grouping by GPAX','GPAX','FRA142')
# create_grouping('Grouping by RANDOM','RANDOM','FRA241')
#
# create_group(1,59340500001,'AB01')
# create_group(1,59340500002,'AB02')
# create_group(1,59340500003,'AB03')
# create_group(1,59340500004,'AB04')
# create_group(1,59340500005,'AB05')
# create_group(1,59340500006,'AB06')
# create_group(1,59340500007,'AB07')
# create_group(1,59340500008,'AB08')
# create_group(1,59340500009,'AB09')
# create_group(1,59340500010,'AB10')
# create_group(1,59340500011,'AB01')
# create_group(1,59340500012,'AB02')
# create_group(1,59340500013,'AB03')
# create_group(1,59340500014,'AB04')
# create_group(1,59340500015,'AB05')
# create_group(1,59340500016,'AB06')
# create_group(1,59340500017,'AB07')
# create_group(1,59340500018,'AB08')
# create_group(1,59340500019,'AB09')
# create_group(1,59340500020,'AB10')
# create_group(2,59340500001,'A01')
# create_group(2,59340500002,'A01')
# create_group(2,59340500003,'A01')
# create_group(2,59340500004,'A01')
# create_group(2,59340500005,'A01')
# create_group(2,59340500006,'B01')
# create_group(2,59340500007,'B01')
# create_group(2,59340500008,'B01')
# create_group(2,59340500009,'B01')
# create_group(2,59340500010,'B01')
#
#
# create_task(1,'Lab1',5)
# create_task(2,'Lab1',5)
# create_task(2,'Lab2',15)
#
# create_score(1,59340500001,5)
# create_score(1,59340500002,4)
# create_score(1,59340500003,3)
# create_score(1,59340500004,2)
# create_score(1,59340500005,1)
# create_score(1,59340500006,5)
# create_score(1,59340500007,4)
# create_score(1,59340500008,3)
# create_score(1,59340500009,2)
# create_score(1,59340500010,1)
# create_score(1,59340500011,5)
# create_score(1,59340500012,4)
# create_score(1,59340500013,3)
# create_score(1,59340500014,2)
# create_score(1,59340500015,1)
# create_score(1,59340500016,5)
# create_score(1,59340500017,4)
# create_score(1,59340500018,3)
# create_score(1,59340500019,2)
# create_score(1,59340500020,1)
# for i in range(1,4):
#     create_enrollment('FRA241', None, i)


# delete_student(59340500005)

# delete_subject('FRA241')

# delete_student_enrollment(59340500060,"FRA241")

# delete_lecturer_enrollment(1,'FRA241')

# delete_score("T001",59340500060)

# delete_task('T001',1)

# delete_grouping(1)

# delete_grouping(1)

# delete_grouping(1)"""

# create_credit('AB01',"FRA241",80)
