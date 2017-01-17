# coding: utf8

import mysql.connector

cnx = mysql.connector.connect(user='concordance', password='sosnora',
                              host='concordance.mysql.pythonanywhere-services.com',
                              database='concordance$new', buffered=True)
cursor = cnx.cursor()

query = "SELECT id, word from concordances where id >37000"
cursor.execute(query)
words = cursor.fetchall()
allwords = [[all[0], all[1]] for all in words]

for z in allwords:
    insert = "UPDATE allword SET concordance_number=" + str(z[0]) + " where word = (%s)"
    data = (z[1],)
    cursor.execute(insert, data)
    print z[1]
    cnx.commit()

cursor.close()
cnx.close()