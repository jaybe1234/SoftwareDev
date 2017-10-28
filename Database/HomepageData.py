from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.DatabaseSetup import Base,Student,Lecturer,Enrollment,Grouping,Group,Task,Score,Subject
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
def homepage_data(lecturer_name,subject_code):
    #get lecturer name
    result =[]
    result1 = []
    list_operator = []
    subject_code = session.query(Subject).filter_by(code_subject=subject_code)[0]
    co_operator = session.query(Enrollment).filter_by(subject_enrollment = subject_code)
    for lecturer_id in co_operator:
        if lecturer_id.lecturer_id_enrollment != None:
            name_lecturer_id = session.query(Lecturer).filter_by(id_lecturer = lecturer_id.lecturer_id_enrollment)[0]
            list_operator.append(name_lecturer_id.name_lecturer)
    result1.append(list_operator)
    list_grouping = []
    list_task = []
    grouping = session.query(Grouping).filter_by(subject_grouping = subject_code)
    for somegrouping in grouping:
        list_grouping.append(somegrouping.name_grouping)
        task = session.query(Task).filter_by(grouping_task = somegrouping)
        for task_name in task:
            list_task.append(task_name.name_task)
    result1.append(list_grouping)
    result1.append(list_task)
    list_student = []
    all_student = session.query(Enrollment).filter_by(subject_enrollment = subject_code)
    for student in all_student:
        list_student_info = []
        if student.student_id_enrollment != None:
            student_info = session.query(Student).filter_by(id_student = student.student_id_enrollment)[0]
            list_student_info.append(student_info.id_student)
            list_student_info.append(student_info.name_student)
            list_student.append(list_student_info)
    result.append(result1)
    result.append(list_student)
    return result
print (homepage_data('Mr.Pitiwut','FRA241'))

def task_score(subject_code,task_name,student_id):
    subject_code = session.query(Subject).filter_by(code_subject = subject_code)[0]
    task_objects = session.query(Task).filter_by(name_task = task_name)
    for task_object in task_objects:
        grouping_object = session.query(Grouping).filter_by(id_grouping = task_object.grouping_id_task)[0]
        if grouping_object.subject_grouping == subject_code :
            correct_task = session.query(Task).filter_by(name_task = task_name,grouping_task = grouping_object)[0]
            score = session.query(Score).filter_by(task_score = correct_task)[0].score_score
    return (score)
print (task_score('FRA241','Lab1',59340500060))