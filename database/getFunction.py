from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject,Grouping,Group,Task,Score
from random import randint
from Database.AddData import *
from operator import attrgetter
#from and NameOfPythonFile
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def getgpax(subject_code):
    student = getStudentList(subject_code)
    studentgpax = []
    sortgpax = sorted(student ,key=lambda student: student.gpax_student ,reverse=True)
    for i in sortgpax:
        studentgpax.append(i)
    return studentgpax

def getstudentgpaxscore(tasklist,subjectCode):
    sortgpax = getgpax(subjectCode)
    scorelist = []
    for i in sortgpax:
        student_score = []
        for a in tasklist:
            score = session.query(Score).filter_by(task_id_score = a.id_task)
            for b in score:
                if b.student_id_score == i.id_student:
                    student_score.append(b)
        scorelist.append(student_score)

    return scorelist

def getstudentgroupscore(tasklist,subjectCode,type_sort):
    sortgroup = sortbygroup(subjectCode,type_sort)
    idstu = []
    scorelist = []
    for i in sortgroup:
        for j in i:
            idstu.append(j.student_id_group)
    for i in idstu:
        student_score = []
        for a in tasklist:
            score = session.query(Score).filter_by(task_id_score = a.id_task)
            for b in score:
                if b.student_id_score == i:
                    student_score.append(b)
        scorelist.append(student_score)
    return scorelist


def getstudentnameIngroup(subjectCode,type_sort):
    namegroup = getlistgroupid(subjectCode,type_sort)
    studentListGroup = sortbygroup(subjectCode,type_sort)
    student1group = []
    for i in range(len(studentListGroup)):
        for j in studentListGroup[i]:
            student1group.append(j)
    numberStudent = int(len(student1group) / len(namegroup))
    arr = [[]* numberStudent for j in range(len(namegroup))]
    nameList = []
    for i in range(len(studentListGroup)):
        for a in studentListGroup[i]:
            name = session.query(Student).filter_by(id_student = a.student_id_group).one()
            nameList.append(name.name_student)
    for i in range(len(namegroup)):
        for a in range(0,numberStudent):
            arr[i].append(nameList[0])
            nameList.remove(nameList[0])
    print(arr)

def lenlist(list):
    lenoflist = []
    for i in list:
        lenoflist.append(len(i))
    return lenoflist

def sortbygroup(subject_code,namegroup):
    group = []
    memberIngroup = []
    sorttee = []
    groupname = session.query(Grouping).filter_by(name_grouping = namegroup).one()
    groupid = session.query(Group).filter_by(grouping_id_group = groupname.id_grouping)
    for i in groupid:
            if i.group_id_group not in group:
                group.append(i.group_id_group)
    memberOnegroup = session.query(Group).filter_by(group_id_group = group[0])
    member = session.query(Group).filter_by(grouping_id_group = groupname.id_grouping)
    memberall = []
    for i in memberOnegroup:
        memberIngroup.append(i.student_id_group)
    numMember = len(memberIngroup)
    for i in group:
        arr = [[]* numMember for j in range(len(group))]
    for i in member:
        memberall.append(i)
    #for i in memberall:
    for a in range(len(group)):
        for b in range(numMember):
            arr[a].append(memberall[0])
            memberall.remove(memberall[0])
    for i in arr:
        temp = sorted(i, key = lambda group:group.student_id_group)
        sorttee.append(temp)
    return sorttee


def getlistgroupid(subject_code,namegroup):
    group = []
    groupname = session.query(Grouping).filter_by(name_grouping = namegroup).one()
    groupid = session.query(Group).filter_by(grouping_id_group = groupname.id_grouping)
    for i in groupid:
            if i.group_id_group not in group:
                group.append(i.group_id_group)
    return group

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
    finalstdlist = sorted(studentList, key=lambda student: student.id_student)
    return finalstdlist

def otherStudentList(subjectCode):
    otherstudent = []
    studentList = getStudentList(subjectCode)
    everystudent = session.query(Student)
    for i in everystudent:
        if i not in studentList:
            otherstudent.append(i)
    return otherstudent

def getLecturerNotinclass(listLecIn):
    lecall = session.query(Lecturer)
    lecOther = []
    for i in lecall:
        if i not in listLecIn:
            lecOther.append(i)
    return lecOther

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
        B = getStudentSection(subjectCode, 'b')
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
                ran = randint(0,len(B)-1)
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
    if group_from == "option1":
        sorted_student = sorted(student, key=lambda student: student.gpax_student)
        remain = len(student) % int(group_num)
        for a in range(group_num - remain):
            for b in range(people_group):
                one = sorted_student[0]
                create_group(grouping_id, one.id_student, group_prefix + '#' + str(a + 1))
                sorted_student.remove(one)
        for a in range(remain):
            for b in range(people_group + 1):
                one = sorted_student[0]
                create_group(grouping_id, one.id_student, group_prefix + '#' + str(a + group_num - remain))
                sorted_student.remove(one)
    elif group_from == "option2":
        A = getStudentSection(subjectCode, 'a')
        B = getStudentSection(subjectCode, 'b')
        sorted_A = sorted(A, key=lambda student: student.gpax_student)
        sorted_B = sorted(B, key=lambda student: student.gpax_student)
        num_group_in_A = int(len(A)/people_group)
        num_group_in_B = int(len(B)/people_group)
        remain_A = len(A) % num_group_in_A
        remain_B = len(B) % num_group_in_B
        for a in range(num_group_in_A - remain_A):
            for b in range(people_group):
                one = sorted_A[0]
                create_group(grouping_id, one.id_student, group_prefix + '_A' + '#' + str(a + 1))
                sorted_A.remove(one)
        for a in range(remain_A):
            for b in range(people_group + 1):
                one = sorted_A[0]
                create_group(grouping_id, one.id_student, group_prefix + '_A' + '#' + str(a + num_group_in_A - remain_A))
                sorted_A.remove(one)
        for a in range(num_group_in_B - remain_B):
            for b in range(people_group):
                one = sorted_B[0]
                create_group(grouping_id, one.id_student, group_prefix + '_B' + '#' + str(a + 1))
                sorted_B.remove(one)
        for a in range(remain_B):
            for b in range(people_group + 1):
                one = sorted_B[0]
                create_group(grouping_id, one.id_student, group_prefix + '_B' + '#' + str(a + num_group_in_B - remain_B))
                sorted_B.remove(one)



def grouping_studentid(group_from,group_num,subjectCode,grouping_name, group_prefix):
    student = getStudentList(subjectCode)
    people_group = int(len(student) / int(group_num))
    create_grouping(grouping_name,'GPAX',subjectCode)
    grouping = session.query(Grouping).filter_by(subject_code_grouping = subjectCode)
    for i in grouping:
        if i.name_grouping == grouping_name:
            grouping_id = i.id_grouping
            break
    if group_from == "option1":
        sorted_student = sorted(student, key=lambda student: student.id_student)
        remain = len(student) % int(group_num)
        for a in range(group_num - remain):
            for b in range(people_group):
                one = sorted_student[0]
                create_group(grouping_id, one.id_student, group_prefix + '#' + str(a + 1))
                sorted_student.remove(one)
        for a in range(remain):
            for b in range(people_group + 1):
                one = sorted_student[0]
                create_group(grouping_id, one.id_student, group_prefix + '#' + str(a + group_num - remain))
                sorted_student.remove(one)
    elif group_from == "option2":
        A = getStudentSection(subjectCode, 'a')
        B = getStudentSection(subjectCode, 'b')
        sorted_A = sorted(A, key=lambda student: student.id_student)
        sorted_B = sorted(B, key=lambda student: student.id_student)
        num_group_in_A = int(len(A)/people_group)
        num_group_in_B = int(len(B)/people_group)
        remain_A = len(A) % num_group_in_A
        remain_B = len(B) % num_group_in_B
        for a in range(num_group_in_A - remain_A):
            for b in range(people_group):
                one = sorted_A[0]
                create_group(grouping_id, one.id_student, group_prefix + '_A' + '#' + str(a + 1))
                sorted_A.remove(one)
        for a in range(remain_A):
            for b in range(people_group + 1):
                one = sorted_A[0]
                create_group(grouping_id, one.id_student, group_prefix + '_A' + '#' + str(a + num_group_in_A - remain_A))
                sorted_A.remove(one)
        for a in range(num_group_in_B - remain_B):
            for b in range(people_group):
                one = sorted_B[0]
                create_group(grouping_id, one.id_student, group_prefix + '_B' + '#' + str(a + 1))
                sorted_B.remove(one)
        for a in range(remain_B):
            for b in range(people_group + 1):
                one = sorted_B[0]
                create_group(grouping_id, one.id_student, group_prefix + '_B' + '#' + str(a + num_group_in_B - remain_B))
                sorted_B.remove(one)

def getGroupList(subject_code, grouping_name):
    grouping = session.query(Grouping).filter_by(name_grouping = grouping_name, subject_code_grouping = subject_code).one()
    grouplist = session.query(Group).filter_by(grouping_id_group = grouping.id_grouping)
    name_group_list = []
    for i in grouplist:
        if i.group_id_group not in name_group_list:
            name_group_list.append(i.group_id_group)
    return name_group_list

def studentInGroupList(subject_code,grouping_name,getgrouplist):
    grouping = session.query(Grouping).filter_by(name_grouping = grouping_name, subject_code_grouping = subject_code).one()
    member_group = []
    for i in getgrouplist:
        member = []
        group = list(session.query(Group).filter_by(group_id_group = i, grouping_id_group = grouping.id_grouping))
        for a in group:
            student = session.query(Student).filter_by(id_student = a.student_id_group).one()
            member.append(student)
        member_group.append(member)
    return member_group

def lenInList(lis):
    num_list = []
    for i in lis:
        num_list.append(len(i))
    return num_list