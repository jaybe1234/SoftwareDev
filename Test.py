import os
import smtplib
import random
from email.mime.text import MIMEText
from flask import Flask, render_template, redirect, request, url_for, flash
from Database.DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject,Grouping,Group,Task,Score,Credit
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

student = getStudentList("FRA241")

sort = sorted(student, key=lambda student: student.gpax_student)
for i in sort:
    print(i.gpax_student)
for i in student:
    print(i.gpax_student)