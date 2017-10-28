from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DatabaseSetup import Base,Lecturer,Enrollment
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def subjectpage_data(lecturer_name):
    result = []
    lecturer_id = session.query(Lecturer).filter_by(name_lecturer = lecturer_name)[0].id_lecturer
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

# print (subjectpage_data('Mr.Pitiwut'))