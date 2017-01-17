# coding: utf8
# попробовать что-либо вида
import json, re
import itertools
from tokenize1 import *
import nltk


def index():
    filename = '/home/concordance/web2py/applications/test/rhymes/stress/t3.txt'
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

def stress():
    filename = '/home/concordance/web2py/applications/test/rhymes/1.txt'
    text = open(filename, 'r').readlines()
    textlines = []
    scheme = []
    for line in text:
        line = line.replace('«', '')
        line = line.replace('»', '')
        words = nltk.word_tokenize(line.decode('utf-8').lower())
        words_new=[]
        for all in words:
            w = d(d.stress.form==all).select().first()
            if w:
                words_new.append(w.stress.decode('utf-8'))
            else:
                words_new.append(all)
        line = ' '.join(words_new)
        metr = re.sub(u'[.|,|—|?|«|»|;|:|-|!| ]', '', line, flags=re.U)
        metr = re.sub(u".'|ё", '— '.decode('utf-8'), metr, flags=re.U)
        #metr = re.sub(u'ё', '— '.decode('utf-8'), metr, flags=re.U)
        metr = re.sub(u'а|о|е|и|у|ю|я|ы|э', 'U ', metr, flags=re.U)
        metr = re.sub(u'[а-я]', '', metr, flags=re.U)
        scheme.append(metr)
        textlines.append(line)
        ikts = [all.count('—'.decode('utf-8')) for all in scheme]
        st = max(ikts)
    return dict(textlines=textlines, metr = scheme, ikts=ikts, st=st)

def stress_db():
    filename = '/home/concordance/web2py/applications/test/rhymes/stress/zh.json'
    with open(filename, 'rb') as outfile:
        dd = json.load(outfile)
    l = []
    for key, i in dd.items():
        for word, s in i.items():
            #l.append([key, word, s])
            d.stress.insert(lemma = key, form = word, stress = s)
    msg = "Все"
    return dict(msg=msg)
