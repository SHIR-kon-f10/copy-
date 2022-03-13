import psycopg2
import random

lot = []
popblocks = ['Mathematics', 'Biology', 'Recently seen', 'Moscow']
randomblocks = ['Математика', 'Биология', 'История', 'Москва', 'Санкт-Петербург', 'ВСОШ', 'IMO', 'Информатика', 'Самара', 'Дистанционно', 'Очно']


conn = psycopg2.connect(database="postgres",
                        user="postgres",
                        password="admin", 
                        host="localhost",
                        port="5432")

cursor = conn.cursor()



def beta():
    currentblocks  = []
    for i in range(4):
        currentblocks.append(randomblocks[random.randint(0,len(randomblocks)-1)])
    print('current' + str(currentblocks))
    tag = ''
    list_of_forms = []
    for i in range(len(currentblocks)):
        tag = currentblocks[i]
        cursor.execute("SELECT * FROM forms WHERE subject = '{0}' OR tag1 = '{0}' OR tag2 = '{0}' OR tag3 = '{0}' OR tag4 = '{0}'OR tag5 = '{0}' OR tag6 = '{0}' OR tag7 = '{0}' OR tag8 = '{0}';".format(tag))
        records = cursor.fetchall()
        for row in records:
            for i in range(4):
                list_of_forms.append(row[i])
    print(list_of_forms)

def popular():
    tag = ''
    list_of_forms = []
    for i in range(len(popblocks)):
        tag = popblocks[i]
        cursor.execute("SELECT * FROM forms WHERE lot = {0};".format(tag))
        records = cursor.fetchall()
        for row in records:
            for i in range(5):
                list_of_forms.append(row[i])
                print(i)
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

beta()
#collect()
#print(lot)