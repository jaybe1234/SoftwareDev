import os
from flask import Flask , render_template , request , redirect , url_for
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
        grouping_id_task = session.query(Task).filter_by(name_task=task_name)
        for i in grouping_id_task:
            if i.grouping_task.subject_code_grouping == subject_code:
                grouping_object = i.grouping_task
                group_id = session.query(Group).filter_by(grouping_group = grouping_object,student_id_group = student_id)[0].group_id_group
                print group_id
                credit = session.query(Credit).filter_by(group_id_credit = group_id)[0].credit
            return redirect(url_for('member',student_id = student_id,subject_code = subject_code,task_name=task_name,credit_bank=credit))
    else:
        return render_template('04_creditbank-login_esthub.html',subject_code=subject_code,task_name=task_name)

@app.route('/students/<string:subject_code>/<string:task_name>/<int:student_id>/<int:credit_bank>/')
def member(subject_code,task_name,student_id,credit_bank):
    grouping_id_task = session.query(Task).filter_by(name_task=task_name)
    for i in grouping_id_task:
        if i.grouping_task.subject_code_grouping == subject_code:
            result_object = i
    group_id_task = session.query(Group).filter_by(grouping_id_group=result_object.grouping_id_task, student_id_group=student_id)[0].group_id_group
    groups = session.query(Group).filter_by(group_id_group=group_id_task)
    return render_template('creditbank_esthub.html',groups=groups,credit_bank=credit_bank)
if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0',port = 5000)
