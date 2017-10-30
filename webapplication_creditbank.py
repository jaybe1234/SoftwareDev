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

@app.route('/students/<string:subject_code>/<string:task_name>/',methods=['GET','POST'])
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
                return redirect(url_for('submitcode',student_id = student_id,subject_code = subject_code,task_name=task_name,credit_bank=credit,number=0))
    else:
        return render_template('04_creditbank-login.html',subject_code=subject_code,task_name=task_name)
@app.route('/students/<string:subject_code>/<string:task_name>/<int:student_id>/<int:credit_bank>/verify/<int:number>/',methods=['GET','POST'])
def submitcode(subject_code,task_name,student_id,credit_bank,number):
    code = 'verify'
    if request.method == 'POST':
        submit_code = request.form['E-mail address']
        if submit_code == code:
            return redirect(url_for('member', student_id=student_id, subject_code=subject_code, task_name=task_name,credit_bank=credit_bank))
        else:
            number = number + 1
            if number>=4:
                return render_template('04_creditbank-login.html', subject_code=subject_code, task_name=task_name)
            return render_template('04_creditbank-login-submitcode.html', subject_code=subject_code,task_name=task_name, student_id=student_id, credit_bank=credit_bank,number=number)
    else:
        return render_template('04_creditbank-login-submitcode.html', subject_code=subject_code, task_name=task_name,student_id=student_id,credit_bank=credit_bank,number=1)



@app.route('/students/<string:subject_code>/<string:task_name>/<int:student_id>/<int:credit_bank>/',methods=['GET','POST'])
def member(subject_code,task_name,student_id,credit_bank):
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
        score = request.form['E-mail address']
        new_score = session.query(Score).filter_by(score_score = score,task_score=task_object,student_id_score = student_id)
        session.add(new_score)
        session.commit()
        return redirect(url_for('thankyou'))
    else:
        return render_template('04_creditbank.html', groups=groups, credit_bank=credit_bank, student_id=student_id,length=length)

@app.route('/students/thankyou/')
def thankyou():
    return "THANK YOU :)"

if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0',port = 5000)
