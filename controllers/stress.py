# coding: utf8
# попробовать что-либо вида
import json, re
import itertools
from tokenize1 import *
import nltk
from numpy import median, bincount, sum
from collections import Counter

def index():
    filename = '/home/concordance/web2py/applications/test/rhymes/stress/All_Forms.txt'
    with open(filename, 'rb') as f:
        text = f.readlines()
    result = []
    for all in text:
        all=all.replace('\r\n', '')
        split_text = all.split('#')
        word = split_text[0]
        line = split_text[1].split(',')
        for w in line:
            antistress = w.replace("'", '')
            d.stress.insert(lemma = word, form = antistress, stress = w)
            result.append([antistress, w])
    return dict(result=result)
        

def index1():
    filename = '/home/concordance/web2py/applications/test/rhymes/stress/All_Forms.txt'
    with open(filename, 'rb') as f:
        text = f.readlines()
    newlines = []
    words = []
    for all in text:
        all=all.replace('\r\n', '')
        c = all.split('#')
        newlines.append(c)
        words.append(c[0].decode('utf-8'))
    newlines2 = [all[1].split(',') for all in newlines]
    newlines_antistress = []
    newlines_stress = []
    for all in newlines2:
        newlines3 = [n.replace("'", '') for n in all]
        newlines3 = [n.replace("`", '') for n in newlines3]
        #newlines3 = [n.replace("ё", 'е') for n in newlines3]
        newlines_antistress.append(newlines3)
        newlines_stress.append(all)
    couples = []
    paradigma = {}
    err = []
    for a in xrange(0, len(newlines_antistress)-1):
        paradigma[words[a]]={}
        for all in xrange(0, len(newlines_antistress)-1):
            try:
                not_stressed_word = newlines_antistress[a][all]
                stressed_word = newlines_stress[a][all].decode('utf-8')
                c = [not_stressed_word, stressed_word]
                couples.append(c)
                paradigma[words[a]][not_stressed_word]=stressed_word
            except:
                err.append(newlines_antistress[a])
    f = filename.replace('.txt', '.json')
    with open(f, 'w') as outfile:
        json.dump(paradigma, outfile)

    return dict(paradigma = paradigma, err=err)

types = {'— U'.decode('utf-8'): 'хорей', 'U —'.decode('utf-8'): 'ямб', '— U U'.decode('utf-8'): 'дактиль', 'U U —'.decode('utf-8'): 'анапест', 'U — U'.decode('utf-8'): 'амфибрахий'}

def stress():
    text = trymysql(trymysql.text1.id==request.args(0)).select()[0]
    #filename = '/home/concordance/web2py/applications/test/rhymes/1.txt'
    text = open(text.filename, 'r').readlines()
    textlines = []
    scheme = []
    without_stress = []
    for line in text:
        line = line.replace('.«|»', '')
        #line = line.replace('»', '')
        words = nltk.word_tokenize(line.decode('utf-8').lower())
        words_new=[]
        letters = ['а', 'о', 'е', 'и', 'у', 'ю', 'я', 'ы', 'э', 'ё']
        for all in words:
            w = d(d.stress.form==all).select().first()
            if w:
                words_new.append(w.stress.decode('utf-8'))
            else:
                words_new.append(all)
                without_stress.append(all)
        line = ' '.join(words_new)
        metr = re.sub(u'[.|,|—|?|«|»|;|:|-|!|-| ]', '', line, flags=re.U)
        metr = re.sub(u".'|ё", '— '.decode('utf-8'), metr, flags=re.U)
        #metr = re.sub(u'ё', '— '.decode('utf-8'), metr, flags=re.U)
        metr = re.sub(u'а|о|е|и|у|ю|я|ы|э', 'U ', metr, flags=re.U)
        metr = re.sub(u'[а-я]', '', metr, flags=re.U)
        scheme.append(metr)
        textlines.append(line)
    ikts = [all.count('—'.decode('utf-8')) for all in scheme]
    # вычисляем длину стопы
    #for l, v in Counter(ikts).most_common(1):
    #    max_i = l
    max_i = max(ikts,key=ikts.count)
    s = [len(s.replace(' ', '')) for s in scheme] #список длин строк по схеме
    razmer = max(set(s), key=s.count)/max_i # делим длины всех строк на количество ударений, выбираем максимальное
    # определяем метр
    test = [n.replace(' ', '')[:razmer] for n in scheme]
    #if (len(re.sub(u' ', '', n, flags=re.U)))/razmer == max_i]
    result = max(set(test), key = test.count)
    if result == '—U'.decode('utf-8'):
        result = 'хорей'
    if result == 'U—'.decode('utf-8'):
        result = 'ямб'
    if result == '—UU'.decode('utf-8'):
        result = 'дактиль'
    if result == 'UU—'.decode('utf-8'):
        result = 'анапест'
    if result == 'U—U'.decode('utf-8'):
        result = 'амфибрахий'
    if result == '—U—U'.decode('utf-8'):
        result = 'err'
    result = str(max_i) + "-стопный ".decode('utf-8') + result.decode('utf-8')
    return dict(textlines=textlines, scheme = scheme, ikts=ikts, razmer=razmer, test = test, result = result, without_stress=without_stress)

def stress_db():
    filename = '/home/concordance/web2py/applications/test/rhymes/stress/All_Forms.json'
    with open(filename, 'rb') as outfile:
        dd = json.load(outfile)
    l = []
    for key, i in dd.items():
        for word, s in i.items():
            #l.append([key, word, s])
            d.stress.insert(lemma = key, form = word, stress = s)
    msg = "Все"
    return dict(msg=msg)
