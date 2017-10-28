from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.DatabaseSetup import Base,Grouping,Group
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
def create_group(grouping_id,group_id,student_id):
    grouping_id = session.query(Grouping).filter_by(id_grouping=grouping_id)[0]
    new_group = Group(student_id_group = student_id ,group_id_group = group_id, grouping_group = grouping_id)
    session.add(new_group)
    session.commit()
    return