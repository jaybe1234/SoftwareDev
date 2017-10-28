import os
from flask import Flask , render_template , request , redirect , url_for
app = Flask(__name__,template_folder='templates')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject,Grouping,Group,Task,Score
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/students/<string:subject_code>/<string:task_name>/',methods=['GET','POST'])
def login(subject_code,task_name):
    #Find correct Task object
    # grouping_id_task = session.query(Task).filter_by(name_task=task_name)
    # for i in grouping_id_task:
    #     if i.grouping_task.subject_code_grouping == subject_code:
    #         result_object = i
    #Inside GET
    # group_id_task = session.query(Group).filter_by(grouping_id_group = result_object.grouping_id_task,student_id_group = student_id)[0].id_group
    # groups = session.query(Group).filter_by(id_group = grouping_id_task)
    ##
    if request.method == 'POST':
        student_id = request.form['student_id']
        return redirect(url_for('member',student_id = student_id,subject_code = subject_code,task_name=task_name))
        # return render_template('04_creditbank-login.html', subject_code=subject_code, task_name=student_id)
    else:
        return render_template('04_creditbank-login.html',subject_code=subject_code,task_name=task_name)

@app.route('/students/<string:subject_code>/<string:task_name>/<int:student_id>/member/')
def member(subject_code,task_name,student_id):
    # Find correct Task object
    grouping_id_task = session.query(Task).filter_by(name_task=task_name)
    for i in grouping_id_task:
        if i.grouping_task.subject_code_grouping == subject_code:
            result_object = i
    ##
    # Inside GET
    group_id_task = session.query(Group).filter_by(grouping_id_group=result_object.grouping_id_task, student_id_group=student_id)[0].group_id_group
    groups = session.query(Group).filter_by(group_id_group=group_id_task)
    ##
    return render_template('creditbank.html',groups=groups)

@app.route('/')
def onkeyup():
    return render_template('onkeyup.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0',port = 5000)
