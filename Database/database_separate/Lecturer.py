from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.DatabaseSetup import Base,Lecturer,Enrollment
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
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