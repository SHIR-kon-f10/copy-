from flask import Flask, render_template, request, redirect
import psycopg2
import requests
import time

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

            return render_template('account.html', full_name=records[0][1], login='login: '+str(name), password='password: '+str(password))

        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

# Register ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/Sign up/', methods=['POST', 'GET'])
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

# Back --------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/Back/' , methods=['POST','GET'])
def back():
    if request.method == 'POST':

        conn.commit()

        return redirect('/account/')

# Create form -------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/Create form/', methods=['POST', 'GET'])
def create_form():
    if request.method == 'POST':
        title = request.form.get('title')
        maintext = request.form.get('maintext')
        subject = request.form.get('subject')
        grade = request.form.get('grade')
        olimp = request.form.get('olimp')
        lotr = request.form.get('tags')

        if len(title)<16 or len(maintext)<32 or len(subject)==0 or len(grade)==0:
            return render_template('error404.html')
        else:
            cursor.execute('INSERT INTO forms (title, description, course, status, owner, lot) VALUES (%s, %s, %s);', (str(title), str(maintext), str(subject), str(olimp), str(grade), str(lotr)))

            conn.commit()

            return redirect('/account/')

# Log out -----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/log out/', methods=['POST'])
def logout():
    if request.method == 'POST':
        #return redirect('/login/')
        pass

    return render_template('/login/')

# locate to create form ---------------------------------------------------------------------------------------------------------------------------------
@app.route('/ltcf/')
def ltcf():
    if request.method == 'POST':
        pass
    return render_template('/Create form/')