import os
from flask import Flask, render_template, redirect, request
from database.database_setup import Lecturer, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.crud_lecturer import create_lecturer

engine = create_engine('sqlite:///database/main.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)

create_lecturer(1, 'Blink', 'Bawornsak', 'eiei')
@app.route("/")
@app.route("/login", methods = ['GET', 'POST'])
def login():
    return render_template('login.html')
@app.route("/login/<str:username>", methods = ['GET','POST'])
def logincheck():
    username = session.query(Lecturer).filter_by(username = request.form['email'])
    if username == request.form['password']:
        return redirect(url_for('02_home.html'))




if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost', port = 5000)