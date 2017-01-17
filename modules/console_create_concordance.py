# coding: utf8

import mysql.connector

cnx = mysql.connector.connect(user='concordance', password='sosnora',
                              host='concordance.mysql.pythonanywhere-services.com',
                              database='concordance$new', buffered=True)
cursor = cnx.cursor()

query = "SELECT word from allword where author = 1"
cursor.execute(query)
words = cursor.fetchall()
allwords = [all[0] for all in words]

for z in allwords:
    try:
        query = "SELECT * from concordances where word = (%s)"
        data = (z,)
        cursor.execute(query, data)
        print "isn't"
    except:
        insert = "INSERT into concordances(word) VALUES (%s)"
        data = (z,)
        cursor.execute(insert, data)
        print z
        cnx.commit()

cursor.close()
cnx.close()