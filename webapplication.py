import os
import smtplib
import random
from email.mime.text import MIMEText
from flask import Flask, render_template, redirect, request, url_for, flash
from Database.DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject,Grouping,Group,Task,Score,Credit,Storage
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.getFunction import *
from Database.AddData import *
from Database.HomepageData import *
from Database.SubjectPageData import subjectpage_data, getScoreFromTask, totalScore, updateScore

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
def deleteSub(username,subject_code):
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
    else:
        return render_template('karnhomepage.html',username = username,subject = subject,lensub = lensub,nameuser = nameuser,sub = sub,all_lec = all_lec)

@app.route('/<string:username>/add_class',methods = ['GET','POST'])
def add_class(username):
    if request.method == 'POST':
        nameuser = session.query(Lecturer).filter_by(user_lecturer = username)
        all_sub = session.query(Subject).filter_by(code_subject = Subject.code_subject)
        subListAll =[]
        lensub = []
        id_user = nameuser[0].id_lecturer
        for i in all_sub:
            subListAll.append(i.code_subject)
        nameclass = request.form['classname']
        lec = request.form.getlist('lecturer')
        if nameclass is not None :
            for i in subListAll:
                if nameclass == i:
                    return ("This class's name already exists")
            create_subject(" ",nameclass)
            create_enrollment(nameclass,None,id_user)
            for i in lec:
                create_enrollment(nameclass, None , i )
    return redirect(url_for('home',username= username))

@app.route('/<string:username>/home2',methods = ['GET','POST'])
def home2(username):
    return render_template('bamhompage.html')

@app.route('/<string:username>/<string:subject_code>/movetohome')
def movetohome(username):
    delete_archive(username,subject_code)
    return redirect(url_for('home',username= username))

@app.route('/<string:username>/<string:subject_code>/archive')
def add_archive(username,subject_code):
    create_archive(username,subject_code)
    return redirect(url_for('home',username= username))

@app.route('/<string:username>/archive',methods = ['GET','POST'])
def archive(username):
    if login == False:
        return redirect('login')
    else:
        nameuser = session.query(Lecturer).filter_by(user_lecturer = username)
        id_user = nameuser[0].id_lecturer
        lecnotuser = getlecnotuser(username)
        listarchive = getarchive(id_user)
        len_listarchive = len(listarchive)
        subject = subjectpage_data(username)
        return render_template('Archive.html',username = username,subject = subject,lecnotuser = lecnotuser,listarchive = listarchive,
                                len_listarchive = len_listarchive,nameuser = nameuser)

@app.route('/<string:username>/<string:subject_code>/<string:type_sort>', methods = ['GET' , 'POST'])
def subject(username,subject_code,type_sort):
    subject = subjectpage_data(username)
    studentList = getStudentList(subject_code)
    lecturerList = getLecturerList(subject_code)
    groupingList = getGrouping(subject_code)
    taskList = getTask(subject_code)
    scorelist = getScoreFromTask(taskList, studentList)
    totalscore = totalScore(taskList, studentList)
    nameuser = session.query(Lecturer).filter_by(user_lecturer = username).one()
    range_student = range(len(studentList))
    len_scorelist = len(scorelist)
    len_tasklist = len(taskList)
    lecOther = getLecturerNotinclass(lecturerList)
    lecnotuser = getlecnotuser(username)
    if type_sort == 'studentid':
        return render_template('03_class.html', username = username, subject_code = subject_code,studentList = studentList,
                                lecturerList = lecturerList , groupingList = groupingList ,taskList = taskList,
                                scorelist = scorelist, totalscore = totalscore,range_student = range_student,
                                nameuser = nameuser,subject = subject,len_scorelist = len_scorelist,len_tasklist = len_tasklist,
                                type_sort = type_sort,lecOther = lecOther,lecnotuser = lecnotuser)
    elif type_sort == 'gpax':
        sortgpax = getgpax(subject_code)
        len_sortgpax = len(sortgpax)
        scoreStudentGpax = getstudentgpaxscore(taskList,subject_code)
        return render_template('03_class.html', username = username, subject_code = subject_code,studentList = studentList,
                                lecturerList = lecturerList , groupingList = groupingList ,taskList = taskList,
                                scorelist = scorelist, totalscore = totalscore,range_student = range_student,
                                nameuser = nameuser,subject = subject,len_scorelist = len_scorelist,len_tasklist = len_tasklist,
                                len_sortgpax = len_sortgpax,sortgpax = sortgpax,type_sort = type_sort,scoreStudentGpax = scoreStudentGpax,
                                lecOther = lecOther,lecnotuser = lecnotuser)
    else :
        grouplist = getGroupList(subject_code, type_sort)
        member_group = studentInGroupList(subject_code, type_sort, grouplist)
        len_grouplist = len(grouplist)
        len_member_group = lenInList(member_group)
        namegroup = getlistgroupid(subject_code,type_sort)
        studentListGroup = sortbygroup(subject_code,type_sort)
        len_studentGroup = len(studentListGroup)
        scoregroup = getstudentgroupscore(taskList,subject_code,type_sort)
        len_scoregroup = len(scoregroup)
        groupingtasklist = list(getTaskListFromGrouping(subject_code, type_sort))
        len_groupingtasklist = len(groupingtasklist)
        namestudent_ingroup = getstudentnameIngroup(subject_code,type_sort)
        scorelist = taskListScore(member_group, groupingtasklist)
        len_scorelist = len(scorelist)
        #len_namestudentIngroup = len(namestudent_ingroup)
        return render_template('03_class.html', username = username, subject_code = subject_code,studentList = studentList,
                            lecturerList = lecturerList , groupingList = groupingList ,taskList = taskList,
                            scorelist = scorelist, totalscore = totalscore,range_student = range_student,
                            nameuser = nameuser,subject = subject,len_scorelist = len_scorelist,len_tasklist = len_tasklist,
                            type_sort = type_sort,namegroup = namegroup,len_studentGroup = len_studentGroup,
                            studentListGroup = studentListGroup,scoregroup = scoregroup, len_scoregroup = len_scoregroup,
                            namestudent_ingroup = namestudent_ingroup,lecOther = lecOther, len_grouplist = len_grouplist,
                            len_member_group = len_member_group, grouplist = grouplist, member_group = member_group,
                            len_groupingtasklist = len_groupingtasklist,groupingtasklist = groupingtasklist,lecnotuser = lecnotuser)



@app.route('/<string:username>/<string:subject_code>/addLecturer', methods = ['GET' , 'POST'])
def add_lecturer(username,subject_code):
    if request.method == 'POST':
        lecList = request.form.getlist('otherlec')
        for i in lecList:
            create_enrollment(subject_code,None,i)
    return redirect(url_for('subject', username = username, subject_code = subject_code, type_sort = 'studentid'))


@app.route('/<string:username>/<string:subject_code>/create_grouping', methods = ['GET' , 'POST'])
def create_grouping(username,subject_code):
    if request.method == 'POST':
        if  request.form['grouping_type'] == "random":
            if request.form['optionsRadios'] == "option1":
                grouping_random("option1", int(request.form['group_num']), subject_code,
                                request.form['grouping_name'], request.form['group_prefix'])
                return redirect(url_for('subject', username=username, subject_code=subject_code, type_sort = "studentid"))
            elif request.form['optionsRadios'] == "option2":
                grouping_random("option2", int(request.form['group_num']), subject_code,
                                request.form['grouping_name'], request.form['group_prefix'])
                return redirect(url_for('subject', username=username, subject_code=subject_code, type_sort = "studentid"))
        elif request.form['grouping_type'] == "gpax":
            if request.form['optionsRadios'] == "option1":
                grouping_gpax("option1", int(request.form['group_num']), subject_code,
                                request.form['grouping_name'], request.form['group_prefix'])
                return redirect(url_for('subject', username=username, subject_code=subject_code, type_sort = "studentid"))
            elif request.form['optionsRadios'] == "option2":
                grouping_gpax("option2", int(request.form['group_num']), subject_code,
                                request.form['grouping_name'], request.form['group_prefix'])
                return redirect(url_for('subject', username=username, subject_code=subject_code, type_sort = "studentid"))
        elif request.form['grouping_type'] == "custom":
            if request.form['optionsRadios'] == "option1":
                # return render_template('Custom.html', username = username, subject_code = subject_code,studentList = studentList,
                #                 lecturerList = lecturerList , groupingList = groupingList ,taskList = taskList,
                #                 scorelist = scorelist, totalscore = totalscore,range_student = range_student,
                #                 nameuser = nameuser,subject = subject,len_scorelist = len_scorelist,len_tasklist = len_tasklist)
                return redirect(url_for('custom_grouping',username=username, subject_code=subject_code, type_sort = "studentid" , grouping_name = request.form['grouping_name'] , prefix = request.form['group_prefix']))
            elif request.form['optionsRadios'] == "option2":
                return redirect(url_for('custom_grouping',username=username, subject_code=subject_code, type_sort = "studentid" , grouping_name = request.form['grouping_name'] , prefix = request.form['group_prefix']))
                # return render_template('Custom.html', username = username, subject_code = subject_code,studentList = studentList,
                #                 lecturerList = lecturerList , groupingList = groupingList ,taskList = taskList,
                #                 scorelist = scorelist, totalscore = totalscore,range_student = range_student,
                #                 nameuser = nameuser,subject = subject,len_scorelist = len_scorelist,len_tasklist = len_tasklist)

@app.route('/<string:username>/<string:subject_code>/<string:type_sort>/<string:grouping_name>/<string:prefix>/custom_grouping' , methods = ['GET' , 'POST'])
def custom_grouping(username,subject_code,type_sort,grouping_name,prefix):
    subject = subjectpage_data(username)
    studentList = getStudentList(subject_code)
    lecturerList = getLecturerList(subject_code)
    groupingList = getGrouping(subject_code)
    taskList = getTask(subject_code)
    scorelist = getScoreFromTask(taskList, studentList)
    totalscore = totalScore(taskList, studentList)
    nameuser = session.query(Lecturer).filter_by(user_lecturer = username).one()
    range_student = range(len(studentList))
    len_scorelist = len(scorelist)
    len_tasklist = len(taskList)
    type_sort = "studentid"
    if request.method == 'POST':
        # create_grouping(grouping_name, "Custom" ,subject_code)
        subject_code = session.query(Subject).filter_by(code_subject= subject_code)[0]
        new_grouping = Grouping(name_grouping=grouping_name,type_grouping="custom",subject_grouping=subject_code)
        session.add(new_grouping)
        session.commit()
        for i in range(len(studentList)):
            group_number = request.form[str(i)]
            # return len(studentList)
            subject_code = subject_code.code_subject
            subject_code = session.query(Subject).filter_by(code_subject = subject_code)[0]
            grouping_id = session.query(Grouping).filter_by(name_grouping = grouping_name,subject_grouping = subject_code)[0]
            group_number = prefix + str(group_number)
            create_group(grouping_id.id_grouping,studentList[i].id_student,group_number)
        return redirect(url_for('subject', username=username, subject_code=subject_code.code_subject, type_sort = "studentid"))
    else:
        return render_template('Custom.html', username = username, subject_code = subject_code,studentList = studentList,
                                lecturerList = lecturerList , groupingList = groupingList ,taskList = taskList,
                                scorelist = scorelist, totalscore = totalscore,range_student = range_student,
                                nameuser = nameuser,subject = subject,len_scorelist = len_scorelist,len_tasklist = len_tasklist,type_sort = type_sort ,grouping_name = grouping_name
                                ,prefix=prefix)




@app.route('/<string:username>/<string:subject_code>/add_task' , methods = ['GET' , 'POST'])
def addTask(username, subject_code):
    studentList = getStudentList(subject_code)
    if request.method == 'POST':
        grouping = getGrouping(subject_code)
        if request.form['grouping_name'] == "individual":
            grouping = session.query(Grouping).filter_by(subject_code_grouping = subject_code, name_grouping = 'Individual')
            create_task(None, request.form['task_name'], request.form['score'])
        else:
            create_task(request.form['grouping_name'], request.form['task_name'], request.form['score'])
        tasklist = getTask(subject_code)
        for i in tasklist:
            if i.name_task == request.form['task_name']:
                task = i
                break

        for i in studentList:
            create_score(task.id_task, i.id_student, 0)
    return redirect(url_for('subject', username = username, subject_code = subject_code, type_sort = 'studentid'))

@app.route('/<string:username>/<string:subject_code>/<string:lec_id>/<string:type_sort>/remove_lec', methods = ['GET', 'POST'])
def removeLec(username,subject_code,lec_id,type_sort):
    if request.method == 'POST':
        delete_lecturer_enrollment(lec_id,subject_code)
        return redirect(url_for('subject', username = username, subject_code = subject_code,type_sort = type_sort))

@app.route('/<string:username>/<string:subject_code>/<int:grouping_id>/<string:type_sort>/remove_grouping', methods = ['GET', 'POST'])
def removeGrouping(username,subject_code,grouping_id,type_sort):
    if request.method == 'POST':
        delete_grouping(grouping_id)
        return redirect(url_for('subject', username = username, subject_code = subject_code,type_sort = type_sort ))

@app.route('/<string:username>/<string:subject_code>/<int:task_id>/<string:type_sort>/remove_task', methods = ['GET', 'POST'])
def removeTask(username,subject_code,task_id,type_sort = None):
    if request.method =='POST':
        delete_task(task_id)
        return redirect(url_for('subject', username = username, subject_code = subject_code,type_sort = type_sort))


@app.route('/<string:username>/<string:subject_code>/Manage_student', methods = ['GET', 'POST'])
def manageStudentList(username, subject_code):
    nameuser = session.query(Lecturer).filter_by(user_lecturer = username).one()
    lecturerList = getLecturerList(subject_code)
    groupingList = getGrouping(subject_code)
    taskList = getTask(subject_code)
    nameuser = session.query(Lecturer).filter_by(user_lecturer = username).one()
    studentList = getStudentList(subject_code)
    otherstudent = otherStudentList(subject_code)
    lecOther = getLecturerNotinclass(lecturerList)
    lecnotuser = getlecnotuser(username)
    return render_template('03_manage_student.html', username = username, subject_code = subject_code,
                            lecturerList = lecturerList, groupingList = groupingList, taskList = taskList, studentList = studentList,
                            otherstudent = otherstudent,nameuser = nameuser,lecOther = lecOther,lecnotuser = lecnotuser)



@app.route('/<string:username>/<string:subject_code>/Manage_student/remove_student', methods = ['GET', 'POST'])
def removeStudent(username,subject_code):
    if request.method == 'POST':
        studentlist = request.form.getlist('studentinclass')
        for i in studentlist:
            delete_student_enrollment(i,subject_code)
    return redirect(url_for('manageStudentList', username = username, subject_code = subject_code))

@app.route('/<string:username>/<string:subject_code>/Manage_student/addstudent', methods = ['GET', 'POST'])
def addStudent(username,subject_code):
    if request.method == 'POST':
        studentlist = request.form.getlist('otherstudent')
        for i in studentlist:
            create_enrollment(subject_code,i,None)
        return redirect(url_for('manageStudentList', username = username, subject_code = subject))

@app.route('/<string:username>/<string:subject_code>/<int:student_id>/<string:task_name>/<string:type_sort>/edit' , methods = ['GET' , 'POST'])
def editScore(username,subject_code,student_id,task_name,type_sort):
    student = session.query(Student).filter_by(id_student = student_id).one()
    student_name = student.name_student
    if request.method == 'POST':
        updateScore(student_id, task_name, float(request.form[student_name + task_name]), subject_code)
    return redirect(url_for('subject', username = username, subject_code = subject_code,type_sort = type_sort))

@app.route('/<string:username>/<string:subject_code>/<string:group_name>/<string:task_name>/<string:type_sort>/edit_group_score' , methods = ['GET' , 'POST'])
def editGroupScore(username,subject_code,group_name,task_name,type_sort):
    grouping = session.query(Grouping).filter_by(name_grouping = type_sort, subject_code_grouping = subject_code).one()
    group = session.query(Group).filter_by(group_id_group = group_name,grouping_id_group = grouping.id_grouping)
    if request.method == 'POST':
        for i in group:
            updateScore(i.student_id_group, task_name, float(request.form[i.group_id_group + task_name]), subject_code)
    return redirect(url_for('subject', username = username, subject_code = subject_code,type_sort = type_sort))




@app.route("/<string:subject_code>/<string:task_name>/creditbank",methods=['GET','POST'])
def logincreditbank(subject_code,task_name):
    if request.method == 'POST':
        student_id = request.form['student_id']
        email = request.form['E-mail address']
        # check
        # student id is exist & email adrress is match with student id
        # check_exist_match = session.query(Student).filter_by(email_student = email,student_id = student_id)
        # if len(check_exist_match) == 0:
        #   return render_template('04_creditbank-login.html',subject_code=subject_code,task_name=task_name)
        # else:
        grouping_id_task = session.query(Task).filter_by(name_task=task_name)
        for i in grouping_id_task:
            if i.grouping_task.subject_code_grouping == subject_code:
                grouping_object = i.grouping_task
                group_id = session.query(Group).filter_by(grouping_group = grouping_object,student_id_group = student_id)[0].group_id_group
                credit = session.query(Credit).filter_by(group_id_credit = group_id,task_name_credit = task_name)[0].credit
                code = ''
                alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q','r', 's','t','u', 'v', 'w', 'x', 'y', 'z']
                for i in range(0, 6):
                    number = random.randint(0, 25)
                    code = code + alphabet[number]
                # Create a text/plain message
                msg = MIMEText(code)
                msg['Subject'] = 'SUBMIT CODE FOR CREDITBANK!!'
                # msg['From'] = 's59340500060@hotmail.com'
                # msg['To'] = 'kakan002@hotmail.com'
                s = smtplib.SMTP('smtp.live.com', 587)
                s.ehlo()
                s.starttls()
                s.login('FIBOgradingsystem@hotmail.com', 'Softwaredevelopment')
                s.sendmail('FIBOgradingsystem@hotmail.com', email, '## CODE IS : ' + msg.as_string())
                s.close()
                return redirect(url_for('submitcode',student_id = student_id,subject_code = subject_code,task_name=task_name,credit_bank=credit,number=0,email=email,code=code))
    else:
        return render_template('04_creditbank-login.html',subject_code=subject_code,task_name=task_name)

@app.route("/<string:subject_code>/<string:task_name>/<int:student_id>/<int:credit_bank>/<int:number>/<string:email>/<string:code>/verify",methods=['GET','POST'])
def submitcode(subject_code,task_name,student_id,credit_bank,number,email,code):
    if request.method == 'POST':
        submit_code = request.form['E-mail address']
        if submit_code == code:
            return redirect(url_for('member', student_id=student_id, subject_code=subject_code, task_name=task_name,credit_bank=credit_bank))
        else:
            if number>=4:
                return redirect(url_for('logincreditbank' , subject_code=subject_code , task_name=task_name))
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
            new_storage = Storage(student_id_storage = groups[j].student_id_group , task_name_storage = task_name , score_storage = score )
            # return str(groups[j].student_id_group)
            session.add(new_storage)
            try:
                session.commit()
            except:
               session.rollback()
            score_obj_list = session.query(Storage).filter_by(student_id_storage = groups[j].student_id_group ,task_name_storage = task_name)
            task_id = session.query(Task).filter_by(name_task = task_name)[0].id_task
            score = 0
            score_own = session.query(Score).filter_by(task_id_score = task_id,student_id_score = groups[j].student_id_group)
            if score_own is not None:
                delete_score(task_id,groups[j].student_id_group)
                if score_obj_list is not None:
                    for k in score_obj_list:
                        score = score + k.score_storage
                        create_score(task_id,groups[j].student_id_group,score/8.0)
            # else:
            #     if score_obj_list is not None:
            #         for k in score_obj_list:
            #             score = score + k.score_storage
            #             create_score(task_id,groups[j].student_id_group,score/8.0)
        return redirect(url_for('thankyou'))
    else:
        return render_template('04_creditbank.html', groups=groups, credit_bank=credit_bank, student_id=student_id, length=length,task_name=task_name,subject_code=subject_code)

@app.route('/thankyou')
def thankyou():
    return render_template("testenjoy.html")

if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost', port = 5000)
