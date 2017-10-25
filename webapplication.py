import os
from flask import Flask, render_template, redirect, request, url_for, flash
from database.database_setup import Lecturer, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database/main.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)

login = False
@app.route("/")
@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        user = session.query(Lecturer).filter_by(username = request.form['email'])
        if len(list(user)) == 1:
            if request.form['password'] == user[0].password:
                login = True
                return redirect(url_for('home',username = user[0].username))
            else:
                return redirect('login')
        else:
            return redirect('login')

    else:
        return render_template('01_login.html')


@app.route('/<string:username>/home')
def home(username):
    if login == False:
        return redirect('login')
    else:

        return render_template('02_home.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost', port = 5000)
