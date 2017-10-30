import os
import smtplib
import random
from email.mime.text import MIMEText
from flask import Flask , render_template , request , redirect , url_for ,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject,Grouping,Group,Task,Score,Credit

app = Flask(__name__)
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route("/<string:subject_code>/<string:task_name>",methods=['GET','POST'])
def login(subject_code,task_name):
    if request.method == 'POST':
        student_id = request.form['student_id']
        email = request.form['E-mail address']
        grouping_id_task = session.query(Task).filter_by(name_task=task_name)
        for i in grouping_id_task:
            if i.grouping_task.subject_code_grouping == subject_code:
                grouping_object = i.grouping_task
                group_id = session.query(Group).filter_by(grouping_group = grouping_object,student_id_group = student_id)[0].group_id_group
                credit = session.query(Credit).filter_by(group_id_credit = group_id)[0].credit
                code = ''
                alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                            'r', 's',
                            't',
                            'u', 'v', 'w', 'x', 'y', 'z']
                for i in range(0, 6):
                    number = random.randint(1, 25)
                    code = code + alphabet[number]
                # Create a text/plain message
                msg = MIMEText(code)
                msg['Subject'] = 'SUBMIT CODE FOR CREDITBANK!!'
                msg['From'] = 's59340500060@hotmail.com'
                msg['To'] = 'kakan002@hotmail.com'
                s = smtplib.SMTP('smtp.live.com', 587)
                s.ehlo()
                s.starttls()
                s.login('s59340500060@hotmail.com', '@f36oxeb4S')
                s.sendmail('s59340500060@hotmail.com', email, "## CODE IS : " + msg.as_string())
                s.close()
                return redirect(url_for('submitcode',student_id = student_id,subject_code = subject_code,task_name=task_name,credit_bank=credit,number=0,email=email,code=code))
    else:
        return render_template('04_creditbank-login.html',subject_code=subject_code,task_name=task_name)

@app.route("/<string:subject_code>/<string:task_name>/<int:student_id>/<int:credit_bank>/<int:number>/<string:email>/<string:code>/<verify>",methods=['GET','POST'])
def submitcode(subject_code,task_name,student_id,credit_bank,number,email,code):
    if request.method == 'POST':
        submit_code = request.form['E-mail address']
        if submit_code == code:
            return redirect(url_for('member', student_id=student_id, subject_code=subject_code, task_name=task_name,credit_bank=credit_bank))
        else:
            if number>=4:
                return redirect(url_for('login' , subject_code=subject_code , task_name=task_name))
    number = number + 1
    return render_template('04_creditbank-login-submitcode.html', subject_code=subject_code, task_name=task_name,student_id=student_id,credit_bank=credit_bank,number=number,email = email,code=code)



@app.route('/<string:subject_code>/<string:task_name>/<int:student_id>/<int:credit_bank>/member',methods=['GET','POST'])
def member(subject_code,task_name,student_id,credit_bank):
    # return subject_code
    grouping_id_task = session.query(Task).filter_by(name_task=task_name)
    for i in grouping_id_task:
        if i.grouping_task.subject_code_grouping == subject_code:
            task_object = i
    group_id_task = session.query(Group).filter_by(grouping_id_group=task_object.grouping_id_task, student_id_group=student_id)[0].group_id_group
    groups = session.query(Group).filter_by(group_id_group=group_id_task)
    length = 0
    for i in groups:
        length+=1
    if request.method == 'POST':
        for j in range(length):
            score = request.form[str(j)]
            new_score = Score(score_score = score,task_score=task_object,student_id_score = student_id)
            session.add(new_score)
            session.commit()
        return redirect(url_for('thankyou'))
    else:
        return render_template('04_creditbank.html', groups=groups, credit_bank=credit_bank, student_id=student_id, length=length,task_name=task_name,subject_code=subject_code)

@app.route('/thankyou')
def thankyou():
    return "Enjoy your score :P"


if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0',port = 5000)
