from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.DatabaseSetup import Base,Lecturer,Enrollment,Score,Student,Task
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def subjectpage_data(username):
    result = []
    lecturer_id = session.query(Lecturer).filter_by(user_lecturer = username)[0].id_lecturer
    subjects = session.query(Enrollment).filter_by(lecturer_id_enrollment = lecturer_id)
    for subject in subjects:
        subject_list = []
        subject_code = subject.subject_code_enrollment
        subject_list.append(subject_code)
        other_lecturer = session.query(Enrollment).filter_by(subject_code_enrollment = subject_code)
        for lecturer in other_lecturer:
            co_operator = lecturer.lecturer_id_enrollment
            if (co_operator != None):
                co_operator = session.query(Lecturer).filter_by(id_lecturer = co_operator)[0].name_lecturer
                subject_list.append(co_operator)
        result.append(subject_list)
    return result
def getScoreFromTask(tasklist, student_list):
    scorelist = []
    for i in student_list:
        student_score = []
        for a in tasklist:
            score = session.query(Score).filter_by(task_id_score = a.id_task)
            for b in score:
                if b.student_id_score == i.id_student:
                    student_score.append(b)
        scorelist.append(student_score)
    return scorelist

def totalScore(tasklist, student_list):
    scorelist = []
    for i in student_list:
        x = 0
        for a in tasklist:
            score = session.query(Score).filter_by(task_id_score = a.id_task)
            for b in score:
                if b.student_id_score == i.id_student:
                    x += b.score_score
                    break
        scorelist.append(x)
    return scorelist

def updateScore(student_id, task_name, new_score, subject_code):
    scorelist = session.query(Score).filter_by(student_id_score = student_id)
    tasklist = session.query(Task).filter_by(name_task = task_name)
    for a in scorelist:
        for b in tasklist:
            if int(a.task_id_score) == b.id_task:
                score = a
                break
    score.score_score = new_score
    session.add(score)
    session.commit()
# print (subjectpage_data('Mr.Pitiwut'))
