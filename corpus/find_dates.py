# -*- coding: utf-8 -*-
import mysql.connector
import csv, sys, re

config = {
  'user': 'concordance',
  'password': 'sosnora',
  'host': 'concordance.mysql.pythonanywhere-services.com',
  'database': 'concordance$new ',
  'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config)

cursor = cnx.cursor(buffered=True)

cursor.execute("SELECT year_writing, day_writing, month_writing FROM text1 WHERE id=7635")
test = cursor.fetchone()



cursor.close()

cnx.close()
print test
