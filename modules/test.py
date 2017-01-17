# coding: utf8

from lxml import etree
import mysql.connector
import os
from nltk import wordpunct_tokenize

cnx = mysql.connector.connect(user='concordance', password='sosnora',
                              host='concordance.mysql.pythonanywhere-services.com',
                              database='concordance$new', buffered=True)
cursor = cnx.cursor()
os.chdir('/home/concordance/web2py/applications/test/uploads/xml/8/')


# 4641 for author 2, 9458, 10188, 10261 for author 8,
z = 4269
page = etree.Element('results') # create xml tree
doc = etree.ElementTree(page)
#    texts = trymysql(trymysql.text1.id==int(x)).select().first() # select one poem
query = "SELECT * from text1 WHERE id = " + str(z)
cursor.execute(query)
texts = cursor.fetchone()
#    words_from_base = trymysql(trymysql.allword.title==int(x)).select().first().id # select the poem's words from allword base
query = "SELECT id from allword where title = " + str(z)
cursor.execute(query)
words_from_base = cursor.fetchone()
title = texts[1]
author = texts[18]
f = open(texts[3], 'rb')
content = f.readlines()
f.close()
text = etree.SubElement(page, 'text')
info = etree.SubElement(text, 'info')
one = etree.SubElement(info, 'title').text = title
two = etree.SubElement(info, 'name').text = str(author)
three = etree.SubElement(info, 'author').text = str(author)
poem = etree.SubElement(text, 'poem')
count_stanza = 1                                             # count stanzas
line_count = 1
word_number = words_from_base[0]                       # get first word's id from allword base
stanza = etree.SubElement(poem,  'stanza', number = str(count_stanza))
for lines in content:
    if lines in ['\n', '\r\n']:
        count_stanza += 1
        stanza = etree.SubElement(poem, 'stanza', number = str(count_stanza))
    else:
        string = etree.SubElement(stanza, 'line', number=str(line_count))
        right_line = wordpunct_tokenize(lines.decode('utf-8'))
        line_count +=1
        for word in right_line:
            query = "SELECT * from allword where id = " + str(word_number)
            cursor.execute(query)
            slovo_from_base = cursor.fetchone()
            if slovo_from_base[0] is None:
                slovo = etree.SubElement(string, 'werd', number = str(word_number))
            else:
                query = "SELECT id from allword where title = " + str(z)
                cursor.execute(query)
                ttt = cursor.fetchall()
                t = [all[0] for all in ttt]
                if slovo_from_base[0] in t:
                    slovo = etree.SubElement(string, 'word', number=str(slovo_from_base[0]), pos = slovo_from_base[4]).text=slovo_from_base[2]
                else:
                    pass
            word_number+=1 # update word's id

path = "/home/concordance/web2py/applications/test/uploads/xml/13/"
new_name=path+str(z)+ ".xml"
DECLARATION = """<?xml version="1.0" encoding="utf-8"?>
<?xml-stylesheet type="text/xsl" href="style.xslt"?>\n"""
with open(new_name, 'wb') as output: # would be better to write to temp file and rename
    output.write(DECLARATION)
    doc.write(output, xml_declaration=False, pretty_print=True, encoding='utf-8')
    output.close()

cursor.close()
cnx.close()