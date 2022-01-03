import re
from flask import Flask, render_template, request, redirect
import psycopg2
import requests
import time
import recomendations

app = Flask(__name__)

conn = psycopg2.connect(database="postgres",
                        user="postgres",
                        password="postgresql",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

# login -------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            
            name = request.form.get('username')
            password = request.form.get('password')

            #Исключение на пустые поля
            if len(name)==0 or len(password)==0:
                return render_template('error404.html')

            cursor.execute("SELECT * FROM users WHERE name=%s AND password=%s", (str(name), str(password)))
            records = cursor.fetchall()

            #Исключение на отсутствие пользователя
            if len(records)==0:
                return render_template('error404.html')

            return render_template('homepage.html', full_name=records[0][1], login='login: '+str(name), password='password: '+str(password))

        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

# Register ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        
        #Исключение на пустые поля
        cursor.execute("SELECT * FROM users WHERE name='"+str(login)+"';")

        #замена ненужных символов
        name = name.replace(' ', ',')

        if len(name)==0 or len(login)==0 or len(password)==0:
            return render_template('error404.html')

        #Исключение на пользователя с таким же логином
        elif len(cursor.fetchall()):
            return render_template('error404.html')
        else:
            cursor.execute('INSERT INTO users (lot, name, password) VALUES (%s, %s, %s);', (str(name), str(login), str(password)))

            conn.commit()

            return redirect('/login/')

    return render_template('registration.html')

# Creating form -------------------------------------------------------------------------------------------------------------------------------------
@app.route('/editform/', methods=['POST','GET'])
def createform():
    if request.method == 'POST':
        title = request.form.get('title')
        subject = request.form.get('subject')
        author = request.form.get('author')
        text = request.form.get('maintext')

# Creating recomendations once|day ------------------------------------------------------------------------------------------------------------------
def refresh():
    recomendations.collect()
    recomendations.choose()
    time.sleep(86400)
    refresh()

