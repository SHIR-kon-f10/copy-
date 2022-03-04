from re import S
from flask import Flask, render_template, request, redirect
import psycopg2
from os import getenv
#import ImportDB

conn = psycopg2.connect("postgres://cfqvlkbbmkvspl:db76b82007170e9e662f544552bd4748a3c030a67586a12c061b6c9c2f361bf6@ec2-34-253-29-48.eu-west-1.compute.amazonaws.com:5432/dfpo3tnfniqib6")

app = Flask(__name__)

cursor = conn.cursor()

conn.commit()

current_session = ''

Titles = ['Math']*7
Authors = ['я люблю вареные Яйца']*21
MainTexts = ['sosem']*21
Tags = ['vanilla']*105
Whens = ['3th oct']*21
Subjects = ['maths']*21

# Setting Databases ------------------------------------------------------------------------------------------------------------------------------------
#ImportDB.clear_lot()
#ImportDB.read_lot()
#ImportDB.insert_lot()
# login -------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            
            name = request.form.get('username_or_E-mail')
            password = request.form.get('password')

            #Исключение на пустые поля
            if len(str(name))==0 or len(str(password))==0:
                return render_template('error.html')

            cursor.execute("ROLLBACK;")
            cursor.execute("SELECT * FROM users WHERE name={0} AND password={1};".format("'"+str(name)+"'","'" +str(password)+"'"))
            records = cursor.fetchall()

            #Исключение на отсутствие пользователя
            if len(records)==0:
                return render_template('error.html')
            global current_session
            current_session = name
            return redirect("/homepage/")

        elif request.form.get("registration"):
            return redirect('/registration/')

    return render_template('login.html')

# Register ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    exusern = ''
    if request.method == 'POST':
        if request.form.get("Sign_up"):
            name = request.form.get('Name')
            login = request.form.get('username or E-mail')
            password = request.form.get('password')
            surname = request.form.get('Surname')
            try:
                cursor.execute("ROLLBACK;")
                cursor.execute("SELECT * FROM users WHERE name = {0};".format(str(login)))
                render_template('registration.html', exusern = 'This login is already exists')
            except:
                if len(name)==0 or len(login)==0 or len(password)==0 or len(surname)==0:
                    render_template('registration.html', exusern = 'Fill all gaps')
                else:
                    cursor.execute("ROLLBACK;")
                    cursor.execute("INSERT INTO users (name, email, password, surname) VALUES ({0},"'RH'",{2},{3});".format("'" +str(name)+ "'","'" +str(password)+"'", "'"+str(surname)+"'"))
                    conn.commit()

                    return redirect('/login/')
        if request.form.get("login"):
            return redirect('/login/')
    return render_template('registration.html', exusern = exusern)
# Account -------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/account/', methods=['POST','GET'])
def account():
    if request.method == 'POST':
        if request.form.get("logout"):
            return redirect('/login/')
    return render_template('account.html')
# Create Form ---------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/CreateForm/', methods=['POST', 'GET'])
def create_form():
    username = current_session
    if request.method == 'POST':
        if request.form.get("Create form"):
            title = request.form.get('Title')
            maintext = request.form.get('maintext')
            subject = request.form.get('OlympyadSubject')
            olimp = request.form.get('NameOlympiad')
            lotr = request.form.get('tags')
            contacts = request.form.get('Contacts')
            owner = username

            if len(str(title))<16 or len(str(maintext))<32 or len(str(subject))==0 or len(str(contacts))==0:
                return render_template('error.html')
            else:
                cursor.execute("ROLLBACK;")
                cursor.execute('INSERT INTO forms (title, description, course, status, owner, lot, contacts) VALUES (%s, %s, %s, %s, %s, %s, %s);', (str(title), str(maintext), str(subject), str(olimp), str(owner), str(lotr), str(contacts)))

                conn.commit()

                return redirect('/account/')
    return render_template('CreateForm.html', reqName = username)
# Standart redirect ---------------------------------------------------------------------------------------------------------------------------------------
@app.route('/', methods = ['GET'])
def redirecty():
    return redirect('/login/')
# Home page -----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/homepage/', methods = ['POST','GET'])
def load_recomendations():
    global current_session
    username = current_session
    #global Titles, Authors, MainTexts, Tags, Whens, Subjects
    #cursor.execute('SELECT * FROM users WHERE name = {0};'.format("'"+str(current_session)+"'"))
    #records = cursor.fetchall()
    if request.method == 'POST':
        if request.form.get('click'):
            return redirect('/form/')
        elif request.form.get("login"):
            current_session = username
            return redirect("/CreateForm/")
        elif request.form.get('logout'):
            return redirect('/login/')
    return render_template('HomePage.html', reqName = username, Author1_1 = Authors[0], Author1_2 = Authors[1], Author1_3 = Authors[2], Author2_1 = Authors[3],
        Author2_2 = Authors[4], Author2_3 = Authors[5], Author3_1 = Authors[6], Author3_2 = Authors[7], Author3_3 = Authors[8], Author4_1 = Authors[9], Author4_2 = Authors[10],
        Author4_3 = Authors[11], Title1 = Titles[0], Title2 = Titles[1], Title3 = Titles[2], Title4 = Titles[3], Title5 = Titles[4], Subject1_1 = Subjects[0],
        Subject1_2 = Subjects[1], Subject1_3 = Subjects[2], Subject2_1 = Subjects[3], Subject2_2 = Subjects[4], Subject2_3 = Subjects[5], Subject3_1 = Subjects[6],
        Subject3_2 = Subjects[7], Subject3_3 = Subjects[8], Subject4_1 = Subjects[9], Subject4_2 = Subjects[10], Subject4_3 = Subjects[11], When1_1 = Whens[0],
        When1_2 = Whens[1], When1_3 = Whens[2], When2_1 = Whens[3], When2_2 = Whens[4], When2_3 = Whens[5], When3_1 = Whens[6], When3_2 = Whens[7], When3_3 = Whens[8],
        When4_1 = Whens[9], When4_2 = Whens[10], When4_3 = Whens[11], MainText1_1 = MainTexts[0], MainText1_2 = MainTexts[1], MainText1_3 = MainTexts[2],
        MainText2_1 = MainTexts[3], MainText2_2 = MainTexts[4], MainText2_3 = MainTexts[5], MainText3_1 = MainTexts[6], MainText3_2 = MainTexts[7], MainText3_3 = MainTexts[8],
        MainText4_1 = MainTexts[9], MainText4_2 = MainTexts[10], MainText4_3 = MainTexts[11], Tag1_1_1 = Tags[0], Tag1_1_2 = Tags[1], Tag1_1_3 = Tags[2], Tag1_1_4 = Tags[3],
        Tag1_1_5 = Tags[4], Tag1_2_1 = Tags[5], Tag1_2_2 = Tags[5], Tag1_2_3 = Tags[6], Tag1_2_4 = Tags[7], Tag1_2_5 = Tags[8], Tag1_3_1 = Tags[9], Tag1_3_2 = Tags[10],
        Tag1_3_3 = Tags[11], Tag1_3_4 = Tags[12], Tag1_3_5 = Tags[13], Tag1_4_1 = Tags[14], Tag1_4_2 = Tags[15], Tag1_4_3 = Tags[16], Tag1_4_4 = Tags[17], Tag1_4_5 = Tags[18],
        Tag2_1_1 = Tags[19], Tag2_1_2 = Tags[20], Tag2_1_3 = Tags[21], Tag2_1_4 = Tags[22], Tag2_1_5 = Tags[23], Tag2_2_1 = Tags[24], Tag2_2_2 = Tags[25], Tag2_2_3 = Tags[26],
        Tag2_2_4 = Tags[27], Tag2_2_5 = Tags[28], Tag2_3_1 = Tags[29], Tag2_3_2 = Tags[30], Tag2_3_3 = Tags[31], Tag2_3_4 = Tags[32], Tag2_3_5 = Tags[33], Tag2_4_1 = Tags[34],
        Tag2_4_2 = Tags[35], Tag2_4_3 = Tags[36], Tag2_4_4 = Tags[37], Tag2_4_5 = Tags[38], Tag3_1_1 = Tags[39], Tag3_1_2 = Tags[40], Tag3_1_3 = Tags[41], Tag3_1_4 = Tags[42],
        Tag3_1_5 = Tags[43], Tag3_2_1 = Tags[44], Tag3_2_2 = Tags[45], Tag3_2_3 = Tags[46], Tag3_2_4 = Tags[47], Tag3_2_5 = Tags[48], Tag3_3_1 = Tags[49], Tag3_3_2 = Tags[50],
        Tag3_3_3 = Tags[51], Tag3_3_4 = Tags[52], Tag3_3_5 = Tags[53], Tag3_4_1 = Tags[54], Tag3_4_2 = Tags[55], Tag3_4_3 = Tags[56], Tag3_4_4 = Tags[57], Tag3_4_5 = Tags[58],
        Tag4_1_1 = Tags[59], Tag4_1_2 = Tags[60], Tag4_1_3 = Tags[61], Tag4_1_4 = Tags[62], Tag4_1_5 = Tags[63], Tag4_2_1 = Tags[64], Tag4_2_2 = Tags[65], Tag4_2_3 = Tags[66],
        Tag4_2_4 = Tags[67], Tag4_2_5 = Tags[68], Tag4_3_1 = Tags[69], Tag4_3_2 = Tags[70], Tag4_3_3 = Tags[71], Tag4_3_4 = Tags[72], Tag4_3_5 = Tags[73], Tag4_4_1 = Tags[74],
        Tag4_4_2 = Tags[75], Tag4_4_3 = Tags[76], Tag4_4_4 = Tags[77], Tag4_4_5 = Tags[78])