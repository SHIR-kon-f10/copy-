from flask import Flask, render_template, request, redirect
import psycopg2
import requests

app = Flask(__name__)

conn = psycopg2.connect(database="postgres",
                        user="postgres",
                        password="postgresql",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

#login
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

    return render_template('homepage.html')

#Register
@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        
        #Исключение на пустые поля
        cursor.execute("SELECT * FROM users WHERE name='"+str(login)+"';")

        if len(name)==0 or len(login)==0 or len(password)==0:
            return render_template('error404.html')

        #Исключение на пользователя с таким же логином
        elif len(cursor.fetchall()):
            return render_template('error404.html')
        else:
            cursor.execute('INSERT INTO users (fb, name, password) VALUES (%s, %s, %s);', (str(name), str(login), str(password)))

            conn.commit()

            return redirect('/login/')

    return render_template('registration.html')