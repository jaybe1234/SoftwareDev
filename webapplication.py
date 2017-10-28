import os
from flask import Flask, render_template, redirect, request, url_for, flash
from Database.DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject,Grouping,Group,Task,Score
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
<<<<<<< HEAD
from Database.getFunction import getStudentList, getLecturerList , getGrouping , getTask, grouping_random
from Database.AddData import create_grouping
=======
from Database.getFunction import *
from Database.AddData import *
from Database.HomepageData import *
from Database.SubjectPageData import subjectpage_data
>>>>>>> 534b543cbe75c05df529dbc8ee2727325b669eee

engine = create_engine('sqlite:///database.db')
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
    subject = subjectpage_data(username)
    lensub = []
    lensub.append(len(subject))
    for i in subject:
        lensub.append(len(i))
    if login == False:
        return redirect('login')
    else:
        return render_template('karnhomepage.html',username = username,subject = subject,lensub = lensub)

@app.route('/<string:username>/<string:subject_code>' , methods = ['GET' , 'POST'])
def subject(username,subject_code):
    studentList = getStudentList(subject_code)
    lecturerList = getLecturerList(subject_code)
    groupingList = getGrouping(subject_code)
    taskList = getTask(subject_code)
    if login == False:
        return redirect('login')
    elif request.method == 'POST':
        if request.form['optionsRadios'] == "option1":
            grouping_random("option1", int(request.form['group_num']), subject_code,
                            request.form['groping_id'], request.form['group_prefix'])
            #grouping_random(group_from, group_num, subjectCode, grouping_id, group_id):
            return redirect(url_for('subject',username, subject_code))
        elif request.form['optionsRadios'] == "option2":
            return  redirect(url_for('subject',username, subject_code))
    else:
        return render_template('03_class_copy.html', username = username, subject_code = subject_code,
                               studentList = studentList,lecturerList = lecturerList , groupingList = groupingList ,
                               taskList = taskList)

if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost', port = 5000)
