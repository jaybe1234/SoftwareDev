import os
from flask import Flask, render_template, redirect, request, url_for, flash
from Database.DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject,Grouping,Group,Task,Score
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.getFunction import *
from Database.AddData import *
from Database.HomepageData import *
from Database.SubjectPageData import subjectpage_data, getScoreFromTask, totalScore

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

@app.route('/<string:username>/<string:subject_code>/home/delete')
def delete(username,subject_code):
    delete_subject(subject_code)
    return redirect(url_for('home',username= username))

@app.route('/<string:username>/home',methods = ['GET','POST'])
def home(username):
    sub = []
    lensub = []
    nameuser = session.query(Lecturer).filter_by(user_lecturer = username)
    id_user = nameuser[0].id_lecturer
    subject = subjectpage_data(username)
    lensub.append(len(subject))
    all_lec = session.query(Lecturer).filter_by(name_lecturer = Lecturer.name_lecturer)
    all_sub = session.query(Subject).filter_by(code_subject = Subject.code_subject)
    subListAll =[]
    for i in all_sub:
        subListAll.append(i.code_subject)
    for i in subject:
        lensub.append(len(i))
        namesub = session.query(Subject).filter_by(code_subject = i[0])
        sub.append(namesub[0].name_subject)
    if login == False:
        return redirect('login')
    elif request.method == 'POST' :
        nameclass = request.form['Class_name']
        if nameclass is not None :
            for i in subListAll:
                if nameclass == i:
                    return ("already have this class's name")
            create_subject(" ",nameclass)
            create_enrollment(nameclass, None , id_user )
        return redirect(url_for('home',username= username))
    else:
        return render_template('karnhomepage.html',username = username,subject = subject,lensub = lensub,nameuser = nameuser,sub = sub,all_lec = all_lec)

@app.route('/<string:username>/<string:subject_code>' , methods = ['GET' , 'POST'])
def subject(username,subject_code):
    subject = subjectpage_data(username)
    studentList = getStudentList(subject_code)
    lecturerList = getLecturerList(subject_code)
    groupingList = getGrouping(subject_code)
    taskList = getTask(subject_code)
    scorelist = getScoreFromTask(taskList, studentList)
    totalscore = totalScore(taskList, studentList)
    nameuser = session.query(Lecturer).filter_by(user_lecturer = username)
    range_student = range(len(studentList))
    if login == False:
        return redirect('login')
    elif request.method == 'POST':
    #create grouping
        if request.form['optionsRadios'] == "option1":
            grouping_random("option1", int(request.form['group_num']), subject_code,
                            request.form['grouping_name'], request.form['group_prefix'])
            return redirect(url_for('subject',username = username, subject_code = subject_code))
        elif request.form['optionsRadios'] == "option2":
            grouping_random("option2", int(request.form['group_num']), subject_code,
                            request.form['grouping_name'], request.form['group_prefix'])
            return  redirect(url_for('subject',username = username, subject_code = subject_code))
    #add task
    else:
        return render_template('03_class.html', username = username, subject_code = subject_code,
                               studentList = studentList,lecturerList = lecturerList , groupingList = groupingList ,
                               taskList = taskList, scorelist = scorelist, totalscore = totalscore,
                               range_student = range_student,nameuser = nameuser,subject = subject)

@app.route('/<string:username>/<string:subject_code>/add_task' , methods = ['GET' , 'POST'])
def addTask(username, subject_code):
    studentList = getStudentList(subject_code)
    if request.method == 'POST':
        grouping = getGrouping(subject_code)
        for i in grouping:
            if i.name_grouping == request.form['grouping_name']:
                grouping_id = i.id_grouping
                break
        create_task(grouping_id, request.form['task_name'], request.form['score'])
        tasklist = getTask(subject_code)
        for i in tasklist:
            if i.name_task == request.form['task_name']:
                task = i
                break
        for i in studentList:
            create_score(task.id_task, i.id_student, 0)
    return redirect(url_for('subject', username = username, subject_code = subject_code))



if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost', port = 5000)
