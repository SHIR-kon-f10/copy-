import psycopg2

lot = []
popblocks = []


conn = psycopg2.connect(database="postgres",
                        user="postgres",
                        password="postgresql",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

def popular():
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