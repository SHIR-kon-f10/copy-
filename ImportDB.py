import psycopg2


conn = psycopg2.connect(database="postgres",
                        user="postgres",
                        password="admin",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


conn.commit()

lines = []
LinesArray = []

title = []
description = []
TagTypee = []

title = [] 
color = []

def clear_lot():
    cursor.execute("TRUNCATE TABLE tags;")
    #cursor.execute("create table tags (id serial, title varchar(50), description varchar(150), Tagtype varchar(15));")
    #cursor.execute("DELETE FROM tags;")
def read_lot():
    global lines, title, description, TagTypee, LinesArray
    file = open('ListOfTags.txt', 'r' )
    lines = file.readlines()
    for i in range(len(lines)):
        LinesArray = lines[i].split('|')
        title.append(LinesArray[0])
        description.append(LinesArray[1])
        TagTypee.append(LinesArray[2])
        TagTypee[i] = TagTypee[i].strip()
def insert_lot():
    for i in range(len(title)):
        cursor.execute("ROLLBACK;")
        cursor.execute("INSERT INTO tags (title, description, tagtype) VALUES ({0},{1},'{2}');".format("'"+title[i]+"'","'" +description[i]+"'",TagTypee[i]))
        #cursor.execute('INSERT INTO tags (title, description, tagtype) VALUES ({0},{1},'"1"');'.format("'"+title[i]+"'","'" +description[i]+"'"))
def clear_tot():
    cursor.execute("TRUNCATE TABLE types_of_tags;")
    #cursor.execute("create table tags (id serial, title varchar(50), description varchar(150), Tagtype varchar(15));")
    #cursor.execute("DELETE FROM tags;")
def read_tot():
    global lines, title, color, LinesArray
    file = open('TypesOfTags.txt', 'r' )
    lines = file.readlines()
    for i in range(len(lines)):
        LinesArray = lines[i].split('|')
        title.append(LinesArray[0])
        color.append(LinesArray[1])
        color[i] = color[i].strip()
def insert_tot():
    for i in range(len(title)):
        cursor.execute("ROLLBACK;")
        cursor.execute("INSERT INTO types_of_tags (title, color) VALUES ('{0}','{1}');".format(title[i],color[i]))
        #cursor.execute('INSERT INTO tags (title, description, tagtype) VALUES ({0},{1},'"1"');'.format("'"+title[i]+"'","'" +description[i]+"'"))
#clear_tot()
#read_tot()
insert_tot()
#clear_lot()
#read_lot()
#insert_lot()