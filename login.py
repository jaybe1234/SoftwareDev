from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup_user import Base,User,Password

app = Flask(__name__)

engine = create_engine('sqlite:///account.db')
Base.metadata = engine

DBsession = sessionmaker(bind = engine)
session = DBsession()

@app.route('/')
def correct():
    message = ""
    message += "<html><body>Login Success!</body></html>"
    print  (message)
    return

@app.route('/login',methods=['GET', 'POST'])
def checklogin():
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        if p == relationship(u):
            return redirect(url_for('correct', restaurant_id=restaurant_id))
    else:
        return render_template('Login.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
