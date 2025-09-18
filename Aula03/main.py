from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from models import User, Base, engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

Session = sessionmaker(bind=engine)
session = Session()

def consulta_banco(username, password):
    user =  session.query(User).filter_by(username=username, password=password).first()
    if not user:
        return False
    return True

@app.route('/home')
def home():
    return "Hello, World!"

@app.route('/user/create')
def create_user():
    return render_template('create_user.html')

@app.route('/user/create', methods=['POST'])
def create_user_do():
    username = request.form['username']
    password = request.form['password']
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()
    return redirect(url_for('form'))

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/user/save', methods=['POST'])
def saveForm():
    user = request.form['username']
    password = request.form['password']
    msgReponse = ""
    if consulta_banco( user, password ):
        msgReponse = "Login Successful"
    else:
        msgReponse = "Login Failed"
    
    return render_template('form.html', msg=msgReponse  )


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True, port=5001)
