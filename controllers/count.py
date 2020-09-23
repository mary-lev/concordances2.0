# coding: utf8
from transliterate import translit
import json
import numpy as np
from operator import itemgetter
from draw_kmeans_plt import *
from categories import *

def index():
    no = [3, 22, 23]
    authors = trymysql(trymysql.author.id>0).select()
    table = {}
    for all in no:
        authors.exclude(lambda row: row.id == all)
    a_numbers = [all.id for all in authors if str(all.id) not in no]
    names = [translit(all.family.decode('utf-8'), reversed=True) for all in authors]
    for all in a_numbers:
        try:
            filename = '/home/concordance/web2py/applications/test/corpus/' + str(all) + '_data.txt'
            d = json.load(open(filename))
            table[all] = d
        except:
            pass
    return dict(table=table, authors=authors)

def count_partos():
    parts=[trymysql((trymysql.allword.partos==all)&(trymysql.allword.author==request.args(0))).count() for all in partos]
    author1=trymysql(trymysql.author.id==request.args(0)).select()[0]
    author=author1['family']
    return dict(parts=parts, author=author)

def count_concordance():
    for all in trymysql((trymysql.concordance.id>13500)&(trymysql.concordance.id<14500)).select():
        summa = trymysql((trymysql.allword.word==all.word)&(trymysql.allword.partos=='NOUN')).count()
        all.update_record(number=int(summa))
    #words1=sorted(set(words1))
    #words1.sort(key = itemgetter(1), reverse = True)
    new=[all.word for all in trymysql(trymysql.concordance.number>500).select()]
    t = type(trymysql(trymysql.concordance.id==100).select()[0].number)
    return dict(new=new, t=t)

def sentence_len(): # count mean of length of centences of the author
    texts = trymysql(trymysql.allword.author==request.args(0)).select()
    part = ['.', '!', '...', '?']
    points = trymysql((trymysql.allword.author==request.args(0))&(trymysql.allword.word.belongs(part))).count()
    words = trymysql(trymysql.allword.author==request.args(0)).count()
    sentence=float(words/(points*1.0))
    return dict(sentence=sentence)

def words_len(): # count mean of length of all words of the author and draw a distribution histogram
    texts = trymysql((trymysql.allword.author==request.args(0))&(trymysql.allword.partos!='None')&(trymysql.allword.partos!="PNCT")).select()
    list_lemma = [len(all.lemma.decode('utf-8')) for all in texts]
    distribution = sorted(set([(all, list_lemma.count(all)) for all in list_lemma]))
    words_length = round(sum(list_lemma)/(len(texts)*1.0), 3)
    return dict(words_length=words_length, distribution=distribution)

def stat_data(): # собираем данные по каждому автору для записи в файл
    #query = ((trymysql.mystem.author==request.args(0))&(trymysql.mystem.partos!='PNCT'))
    a = request.args(0)
    query = trymysql.executesql('SELECT (id) from mystem WHERE author= %s and partos!=%s;', placeholders = (a, 'PNCT',))
    query1 = trymysql.executesql('SELECT (id) from text1 WHERE author=%s;', placeholders = (a,))
    #all_words = trymysql.executesql('SELECT COUNT (id) from mystem WHERE author= %s and partos!=%s;', placeholders =(15, 'PNCT',))
    all_words = len(query)
    all_texts = len(query1)
    data = {}
    data['all_words']=float(all_words)/all_texts
    pun = []
    #punct1 = [all.encode('utf-8') for all in punct]
    #all_pun = trymysql((query1)&(trymysql.mystem.word.belongs(punct))).count()
    pun = trymysql.executesql('SELECT (id) from mystem where (author)=%s and (word) in %s;', placeholders=(a, punct,))
    all_pun = len(pun)
    #all_pun = trymysql.executesql('SELECT COUNT * FROM mystem WHERE word IN %s;', punct1)
    data['all_punct'] = float(all_pun)/all_texts
    data['punct'] = {}
    for all in punct:
        #words = trymysql((query1)&(trymysql.mystem.word==all)).count()
        word = trymysql.executesql('SELECT (id) from mystem where author=%s and word=%s;', placeholders=(a, all,))
        words = len(word)
        data['punct'][all] = float(words)/all_texts

    #length of words (средняя длина слова)
    #words = [all.lemma for all in trymysql(trymysql.mystem.author==a).select()]
    word = trymysql.executesql('select (lemma) from mystem where author=%s and partos!=%s;', placeholders=(a, 'PNCT'))
    len_words = 0
    word = list(word)
    for all in word:
        len_words = len_words+len(all[0])
    lw = float(len_words)/len(word)
    data['len_word'] = lw

    #length of poems
    poems = trymysql(trymysql.text1.author==request.args(0)).select()
    lines = 0
    for all in poems:
        filename = all.filename
        with open(filename, 'r') as f:
            text = f.readlines()
        lines += len(text)
    data['len_poem'] = round(float(lines)/len(poems), 3)

    #words_range (насыщенность словаря)
    #words_word = [all.word for all in trymysql(trymysql.mystem.author==a).select()]
    words_word = trymysql.executesql('select (word) from mystem where author=%s;', placeholders=(a,))
    lemmas = [all[0] for all in words_word]
    lemmas_sort = sorted(set(list(lemmas)))
    w_range = float(len(lemmas_sort)/(len(words_word)*1.0))
    data['w_range'] = w_range

    filename = '/home/concordance/web2py/applications/test/corpus/' + str(request.args(0)) + '_stat.txt'
    json.dump(data, open(filename,'w'))
    short = [all for all in word if len(all) <=2]
    return dict(data=data, all_texts=all_texts, all_pun=all_pun, len_words = len_words, l = len(word))

def table_data(): # собираем морфологические данные по каждому автору и записываем в файл
    query = ((trymysql.mystem.author==request.args(0))&(trymysql.mystem.partos!='PNCT'))
    all_words = trymysql(query).count()
    data = {}
    for all in all_parts:
        data[all[0]] = {}
        for each in all:
            t = trymysql((query)&(trymysql.mystem[all[0]]==each)).count()
            data[all[0]][each] = t
    data['parts'] = {}
    for all in ypartos:
        words = trymysql((query)&(trymysql.mystem.partos==all)).count()
        data['parts'][all]=words
    # %
    proc = {}
    for key, value in data.iteritems():
        proc[key] = {}
        for k, v in value.iteritems():
            proc[key][k] = float(v)/all_words
    filename = '/home/concordance/web2py/applications/test/corpus/' + str(request.args(0)) + '_data.txt'
    json.dump(proc, open(filename,'w'))
    return dict(data=data, proc=proc)

def table_view():
    no = [3, 22, 23]
    authors = trymysql(trymysql.author.id>0).select()
    table = {}
    for all in no:
        authors.exclude(lambda row: row.id == all)
    a_numbers = [all.id for all in authors if str(all.id) not in no]
    names = [translit(all.family.decode('utf-8'), reversed=True) for all in authors]
    for all in a_numbers:
        try:
            filename = '/home/concordance/web2py/applications/test/corpus/' + str(all) + '_data.txt'
            d = json.load(open(filename))
            table[all] = d
        except:
            pass
    data_array = []
    values = []
    for n, all in table.iteritems():
        new_list = []
        for key, value in all.iteritems():
            values.append(value)
            for k, v in value.iteritems():
                new_list.append(v)
        data_array.append(new_list)
    X = np.array(data_array, dtype=float)
    filename = 'authors.png'
    draw(X, names, filename)
    return dict(table=table, authors=authors, data_array=data_array, values=values, i=filename)

def stat_view():
    no = [3, 22, 23]
    authors = trymysql(trymysql.author.id>0).select()
    table = {}
    for all in no:
        authors.exclude(lambda row: row.id == all)
    a_numbers = [all.id for all in authors if str(all.id) not in no]
    names = [translit(all.family.decode('utf-8'), reversed=True) for all in authors]
    for all in a_numbers:
        try:
            filename = '/home/concordance/web2py/applications/test/corpus/' + str(all) + '_stat.txt'
            d = json.load(open(filename))
            table[all] = d
        except:
            pass
    data_array = []
    values = []
    for n, all in table.iteritems():
        new_list = []
        for key, value in all.iteritems():
            if key=='punct':
                for k, v in value.iteritems():
                    new_list.append(v)
            else:
                new_list.append(value)
        data_array.append(new_list)
    X = np.array(data_array, dtype=float)
    filename = 'stat.png'
    draw(X, names, filename)
    return dict(table=table, authors=authors, data_array=data_array, values=values, i=filename)

def stat_table():
    no = [3, 22, 23]
    authors = trymysql(trymysql.author.id>0).select()
    table = {}
    for all in no:
        authors.exclude(lambda row: row.id == all)
    a_numbers = [all.id for all in authors if str(all.id) not in no]
    names = [translit(all.family.decode('utf-8'), reversed=True) for all in authors]
    for all in a_numbers:
        try:
            filename = '/home/concordance/web2py/applications/test/corpus/' + str(all) + '_stat.txt'
            d = json.load(open(filename))
            table[all] = d
        except:
            pass
    return dict(table=table, authors=authors)
