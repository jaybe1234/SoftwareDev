import os
from flask import Flask, render_template, redirect, request, url_for, flash
from database.DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject,Grouping,Group,Task,Score
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.AddData import getStudentList

engine = create_engine('sqlite:///Database/database.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)

login = False
@app.route("/")
@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        user = session.query(Lecturer).filter_by(user_lecturer = request.form['email'])
        if len(list(user)) == 1:
            if request.form['password'] == user[0].password_lecturer:
                login = True
                return redirect(url_for('home',username = user[0].user_lecturer))
            else:
                return redirect('login')
        else:
            return redirect('login')

    else:
        return render_template('01_login.html')

@app.route('/<string:username>/home')
def home(username):
    return redirect(url_for('subject',username = username, subject_code = 'FRA241'))

@app.route('/<string:username>/<string:subject_code>')
def subject(username,subject_code):
    if login == False:
        return redirect('login')
    else:
        return render_template('03_class.html', username = username, subject_code = subject_code, studentList = getStudentList(subject_code))


if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost', port = 5000)
