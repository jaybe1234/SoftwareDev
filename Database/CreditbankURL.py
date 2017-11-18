from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject,Grouping,Group,Task,Score
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

def url(subject_code,task_name,port = None):
    if port != None:
        url = "http://localhost:"+str(port)+"/students/"+subject_code+"/"+task_name+'/'
    else:
        url = "http://localhost:/students/" + subject_code + "/" + task_name + '/'
    return url
print (url("FRA241","Lab1"))
