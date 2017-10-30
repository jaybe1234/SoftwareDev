from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.DatabaseSetup import Base,Lecturer,Enrollment,Score,Student
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
        for a in tasklist:
            x = 0
            student_score = []
            score = session.query(Score).filter_by(task_id_score = a.id_task)
            for b in score:
                if b.student_id_score == i.id_student:
                    student_score.append(b)
                    break
        scorelist.append(student_score)
    return scorelist

def totalScore(tasklist, student_list):
    scorelist = []
    for i in student_list:
        for a in tasklist:
            x = 0
            score = session.query(Score).filter_by(task_id_score = a.id_task)
            for b in score:
                if b.student_id_score == i.id_student:
                    x += b.score_score
                    break
        scorelist.append(x)
    return scorelist

# print (subjectpage_data('Mr.Pitiwut'))
