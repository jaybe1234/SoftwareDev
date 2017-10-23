from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/login')
def login():
    return render_template('01_login.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost', port = 5000)