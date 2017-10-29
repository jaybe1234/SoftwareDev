import os
from flask import Flask , render_template , request , redirect , url_for ,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject,Grouping,Group,Task,Score,Credit
app = Flask(__name__)
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
def onkeyup():
    return render_template('onkeyup_esthub.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0',port = 5000)