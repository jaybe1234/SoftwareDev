from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject,Grouping,Group,Task,Score
from random import randint
from database.AddData import create_group
#from and NameOfPythonFile
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def getStudentList(subjectCode):
    enrollList = session.query(Enrollment).filter_by(subject_code_enrollment = subjectCode)
    studentIdList = []
    studentList =[]
    for i in enrollList:
        if i.student_id_enrollment is not None:
            studentIdList.append(i.student_id_enrollment)
    for i in studentIdList:
        student = session.query(Student).filter_by(id_student = i).one()
        studentList.append(student)
    return studentList

def getLecturerList(subjectCode):
    enrollList = session.query(Enrollment).filter_by(subject_code_enrollment = subjectCode)
    lecturerIdList = []
    lecturerList = []
    for i in enrollList:
        if i.lecturer_id_enrollment is not None:
            lecturerIdList.append(i.lecturer_id_enrollment)
    for i in lecturerIdList:
        lecturer = session.query(Lecturer).filter_by(id_lecturer = i).one()
        lecturerList.append(lecturer)
    return lecturerList

def getGrouping(subjectCode):
    groupingList = session.query(Grouping).filter_by(subject_code_grouping = subjectCode)
    return  groupingList

def getTask(subjectCode):
    groupingList = getGrouping(subjectCode)
    taskList = []
    for i in groupingList:
        task = session.query(Task).filter_by(grouping_id_task = i.id_grouping)
        for a in task:
            taskList.append(a)
    return taskList

def getStudentSection(subjectCode,sec):
    studentList = getStudentList(subjectCode)
    A = []
    B =[]
    for i in studentList:
        if i.section_student == 'A':
            A.append(i)
        elif i.section_student == "B":
            B.append(i)
    if sec == 'a':
        return A
    elif sec == 'b':
        return B

def grouping_random(group_from,group_num,subjectCode,grouping_id, group_id):
    student = getStudentList(subjectCode)
    people_group = len(student) / int(group_num)
    group = [[None] * 1 for i in range(group_num)]
    if group_from == "option1":
        for i in group_num:
            for a in range(people_group):
                ran = randint(len(student)-1)
                one = student[ran]
                student.remove(one)
                create_group(grouping_id,one.id_student,group_id + '#' + str(i+1))
        for i in range(student):
            one = student[i]
            create_group(grouping_id, one.id_student, group_id + '#' + str(i + 1))
    elif group_from == "option2":
        pass




