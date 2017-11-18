from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject,Grouping,Group,Task,Score
from random import randint
from Database.AddData import *
#from and NameOfPythonFile
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def sortbygpax(subject_code):
    student = getStudentList(subject_code)
    idstudent = []
    sortgpax = sorted(student ,key=lambda student: student.gpax_student ,reverse=True)
    for i in sortgpax:
        idstudent.append(i)
    return idstudent

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

def getScorePrimaryKey(subjectCode, student_id, task_name):
    tasklist = getTask(subjectCode)
    score = session.query(Score).filter_by(student_id_score = student_id)
    for a in tasklist:
        for b in score:
            if a.id_task == b.task_id_score:
                primary_key = b.primary_key
                break
    return primary_key


def grouping_random(group_from,group_num,subjectCode,grouping_name, group_prefix):
    student = getStudentList(subjectCode)
    people_group = int(len(student) / int(group_num))
    create_grouping(grouping_name,'RANDOM',subjectCode)
    grouping = session.query(Grouping).filter_by(subject_code_grouping = subjectCode)
    for i in grouping:
        if i.name_grouping == grouping_name:
            grouping_id = i.id_grouping
            break
    if group_from == "option1":
        for i in range(group_num):
            for a in range(people_group):
                ran = randint(0,len(student)-1)
                one = student[ran]
                student.remove(one)
                create_group(grouping_id,one.id_student,group_prefix + '#' + str(i+1))
        for i in range(len(student)):
            one = student[i]
            create_group(grouping_id, one.id_student, group_prefix + '#' + str(i + 1))
    elif group_from == "option2":
        A = getStudentSection(subjectCode, 'a')
        B = getStudentSection(subjectCode, 'a')
        num_group_in_A = int(len(A)/people_group)
        num_group_in_B = int(len(B)/people_group)
        for i in range(num_group_in_A):
            for a in range(people_group):
                ran = randint(0,len(A)-1)
                one = A[ran]
                A.remove(one)
                create_group(grouping_id,one.id_student,group_prefix + '_A' + '#' + str(i+1))
        for i in range(len(A)):
            one = A[i]
            create_group(grouping_id, one.id_student, group_prefix + '_A' + '#' + str(i + 1))
        for i in range(num_group_in_B):
            for a in range(people_group):
                ran = randint(0,len(A)-1)
                one = B[ran]
                B.remove(one)
                create_group(grouping_id, one.id_student, group_prefix + '_B' + '#' + str(i + 1))
        for i in range(len(B)):
            one = B[i]
            create_group(grouping_id, one.id_student, group_prefix + '_B' + '#' + str(i + 1))

def grouping_gpax(group_from,group_num,subjectCode,grouping_name, group_prefix):
    student = getStudentList(subjectCode)
    people_group = int(len(student) / int(group_num))
    create_grouping(grouping_name,'GPAX',subjectCode)
    grouping = session.query(Grouping).filter_by(subject_code_grouping = subjectCode)
    for i in grouping:
        if i.name_grouping == grouping_name:
            grouping_id = i.id_grouping
            break
    if group_fromm == "option1":
        sorted_student = sorted(student, key=lambda student: student.gpax_student)
        remain = len(student) % int(group_num)
        for a in range(group_num - remain):
            for b in range(people_group):
                one = student[0]
                create_group(grouping_id, one.id_student, group_prefix + '#' + str(a + 1))
                student.remove(one)
        for a in range(remain):
            for b in range(people_group + 1):
                one = student[0]
                create_group(grouping_id, one.id_student, group_prefix + '#' + str(a + group_num - remain))
                student.remove(one)
    elif group_from == "option2":
        pass
