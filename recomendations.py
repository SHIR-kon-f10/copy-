import psycopg2

lot = []
popblocks = ['Mathematics', 'Biology', 'Recently seen', 'Moscow']


conn = psycopg2.connect(database="postgres",
                        user="postgres",
                        password="postgresql",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

def popular():
    tag = ''
    list_of_forms = []
    for i in range(len(popblocks)):
        tag = popblocks[i]
        cursor.execute("SELECT * FROM forms WHERE lot = {0};".format(tag))
        records = cursor.fetchall()
        for i in range(5):
            
            list_of_forms.append()
    popblocks.append

def collect():
    lots = []
    cursor.execute("SELECT lot FROM users")
    lots.append(cursor.fetchall())
    for i in range(len(lots)):
        s = ''
        s = lots[i]
        #s = s.split(',')
        lot.append(s)

def choose():
    for i in range(len(lot)):
        pass

collect()
print(lot)