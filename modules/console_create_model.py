# coding: utf8

import mysql.connector
import gensim, logging
from gensim import corpora, models, similarities
from gensim.models import doc2vec

cnx = mysql.connector.connect(user='concordance', password='sosnora',
                              host='concordance.mysql.pythonanywhere-services.com',
                              database='concordance$new', buffered=True)
cursor = cnx.cursor()

query = "SELECT id from text1 where id > 0"
cursor.execute(query)
texts = cursor.fetchall()
sentences = []
for all in texts:
    query1 = "SELECT word from mystem where title=%s and partos!='PNCT'"
    title = all
    cursor.execute(query1, title)
    words = cursor.fetchall()
    wo = []
    for w in words:
        wo.append(w[0])
    sentences.append(wo)

model1 = gensim.models.Word2Vec(sentences, min_count=20, window=30, size=300)
model1.save("/home/concordance/web2py/applications/test/uploads/models/new_model")

cnx.commit()

cursor.close()
cnx.close()
