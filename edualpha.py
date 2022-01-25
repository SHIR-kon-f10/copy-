from re import template
from flask import Flask, render_template, request, redirect
import psycopg2
from os import getenv
from urllib3.util import parse_url

def get_database():
    parsed_url = parse_url(getenv("DATABASE_URL"))

    # Берём из auth имя пользователя и пароль от БД
    username, password = parsed_url.auth.split(':')

    return psycopg2.connect(
        database = parsed_url.path[1:],  # Пропускаем первый "/", так как он не является названием БД
        host=parsed_url.host,
        user=username,
        password=password
    )

app = Flask(__name__)

conn = get_database()

cursor = conn.cursor()

# login -------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            
            name = request.form.get('username_or_E-mail')
            password = request.form.get('password')

            #Исключение на пустые поля
            if len(str(name))==0 or len(str(password))==0:
                return render_template('error404.html')

            cursor.execute("SELECT * FROM users WHERE name=%s AND password=%s", (str(name), str(password)))
            records = cursor.fetchall()

            #Исключение на отсутствие пользователя
            if len(records)==0:
                return render_template('error404.html')

            return redirect("/account/")

        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

# Register ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        if request.form.get("Sign_up"):
            name = request.form.get('Name')
            login = request.form.get('username or E-mail')
            password = request.form.get('password')
            surname = request.form.get('Surname')
            
            #Исключение на пустые поля
            cursor.execute("SELECT * FROM users WHERE name='"+str(login)+"';")

            #замена ненужных символов
            #name = name.replace(' ', ',')

            if len(str(name))==0 or len(str(login))==0 or len(str(password))==0:
                return render_template('error404.html')

            #Исключение на пользователя с таким же логином
            elif len(cursor.fetchall()):
                return render_template('error404.html')
            else:
                cursor.execute('INSERT INTO users (name, email, password, surname) VALUES (%s, %s, %s, %s);', (str(name), str(login), str(password), str(surname)))

                conn.commit()

                return redirect('/login/')
        if request.form.get("login"):
            return redirect('/login/')
    return render_template('registration.html')
# account -------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/account/', methods=['POST','GET'])
def account():
    if request.method == 'POST':
        if request.form.get("CreateForm"):
            return redirect('/CreateaForm/')
        if request.form.get("logout"):
            return redirect('/login/')
    return render_template('account.html')
# Create Form ---------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/CreateaForm/', methods=['POST', 'GET'])
def create_form():
    if request.method == 'POST':
        if request.form.get("Save"):
            title = request.form.get('title')
            maintext = request.form.get('maintext')
            subject = request.form.get('subject')
            grade = request.form.get('grade')
            olimp = request.form.get('olimp')
            lotr = request.form.get('tags')

            if len(str(title))<16 or len(str(maintext))<32 or len(str(subject))==0 or len(str(grade))==0:
                return render_template('error404.html')
            else:
                cursor.execute('INSERT INTO forms (title, description, course, status, owner, lot) VALUES (%s, %s, %s, %s, %s, %s);', (str(title), str(maintext), str(subject), str(olimp), str(grade), str(lotr)))

                conn.commit()

                return redirect('/account/')
    return render_template('CreateForm.html')