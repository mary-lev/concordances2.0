# -*- coding: utf-8 -*-
import nltk
from nltk.collocations import *
import pymorphy2
from operator import itemgetter
import re, codecs, urllib, cStringIO, csv, os
from tokenize1 import *

def index():
    texts = test().select(test.text2.ALL, orderby=test.text2.author)
    return dict(texts=texts)

def texts():
    texts = test().select(test.text2.ALL, orderby=test.text2.title)
    return dict(texts=texts)

def the_text(): # по каждому тексту - доступные опции для анализа статистики
    text = test(test.text2.id==request.args(0)).select().first()
    return dict(text=text)

def show():   # показываем текст
    text = test(test.text2.id==request.args(0)).select().first()
    return dict(text=text)

def author():
    texts = test(test.morpho.author == request.args(0)).select()
    return dict(texts=texts)

def tabliza(): # compare all texts in test.morpho (statistical approach)
    table = test().select(test.morpho.ALL, orderby=test.morpho.author)
    return dict(table=table)

def pos_table(): # compare all text in morphot.pos (POS)
    table = morphot().select(morphot.pos.ALL, orderby=morphot.pos.author)
    return dict(table=table)

def verbs_table():
    table = morphot().select(morphot.verb.ALL, orderby=morphot.verb.author)
    return dict(table=table)

def tokenize(): # prepares text for tokenization (decoding) and sorts resulted list alphabetically
    text2 = test(test.text2.id==request.args(0)).select().first()
    text1 = text2['body'].decode('utf-8')
    tokens= tokenize1(text1)
    normal = normaliz1(tokens)
    tokens_encoded=[n.encode('utf-8') for n in tokens]
    tokens_id=test.tokens.insert(title=text2.title, author=text2.author, tokens=tokens_encoded)
    normal.sort(key = itemgetter(0), reverse = False)
#    lemmas=[n[0].encode('utf-8') for n in normal]
#    slovar_id=test.slovar.insert(title=text2.title, author=text2.author, lemmas=lemmas)
    return dict(normal=normal, text2=text2)

def verbalize(): # count verbs and return top-10 of them
    text2 = test(test.text2.id==request.args(0)).select().first()
    text1 = text2['body'].decode('utf-8')
    tokens = tokenize1(text1)
    verb = verbalize1(tokens)
    return dict(verb=verb, text2=text2)

def compare(): # Сравниваем лексику двух текстов
    text1=test(test.slovar.id==request.args(0)).select()[0]
    text2=test(test.slovar.id==request.args(1)).select()[0]
    lemmas1 = text1.lemmas
    lemmas2=text2.lemmas
    result= sorted(set(lemmas1) - set(lemmas2))
    result2= sorted(set(lemmas2) - set(lemmas1))
    l1 = len(lemmas1)
    l2 = len(lemmas2)
    all = len(lemmas1) - len(result)
    return dict(result=result, result2=result2, l1=l1, l2=l2, all=all, text1=text1, text2=text2)

def index1(): # форма для выбора двух текстов, передает id текста для операци сравнения лексики (compare)
    options = [OPTION(texts.title, _value=texts.id) for texts in test().select(test.slovar.ALL)]
    form=FORM(TABLE(TR("Выберите первый текст",SELECT(*options, _name="first")),
                    TR("Выберите второй текст",SELECT(*options, _name="second")),
                    TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.process().accepted:
        redirect(URL('compare', args = [form.vars['first'], form.vars['second']]))
        response.flash="form accepted"
    return dict(form=form)

def index2(): # форма для выбора автора, передает id автора для вывода информации о нем
    options = [OPTION(texts.family, _value=texts.id) for texts in text().select(text.author.ALL)]
    form=FORM(TABLE(TR("Выберите автора",SELECT(*options, _name="first")),
                    TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.process().accepted:
        redirect(URL('author_data', args = form.vars['first']))
        response.flash="form accepted"
    return dict(form=form)

def author_data(): # выводим информацию по авторам
    texts = text(text.author.id==request.args(0)).select()
    group=text(text.text.author==request.args(0)).select()
    return dict(texts=texts, group=group)

def sort(): # prepares text for tokenization (decoding) and sorts resulted list descending
        text2 = test(test.text2.id==request.args(0)).select().first()
        text1 = text2['body'].decode('utf-8')
        normal = normaliz1(tokenize1(text1))
        normal.sort(key = itemgetter(1), reverse = True)
        return dict(normal=normal, text2=text2)

def morpho():
    text2 = test(test.text2.id==request.args(0)).select().first()
    text1 = text2['body'].decode('utf-8')
    sent = nltk.sent_tokenize(text1)
    stop = [',', '.', ';', ':', '!', '?', '...', '—', '-', '«', '»', '»', '*', '"', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    for s in sent:
        s1 = nltk.wordpunct_tokenize(s)
        s2 = [ss.lower() for ss in s1 if ss not in stop]
        morph = pymorphy2.MorphAnalyzer()
        n = 0
        for slovo in s2:
            forms = morph.normal_forms(slovo)
            n = n+1
            n_id = test.new_form.insert(sentences=s, meaning = slovo.encode('utf-8'), forms=u' '.join(forms).encode('utf-8').strip())
    form = FORM().process()
    if form.accepted:
        redirect(URL('index'))
    texts = test().select(test.new_form.ALL)
    return dict(texts=texts, form=form)

def form1(): # get text from user
    form = SQLFORM(test.text2).process()
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)

def from_file(): # get text from user's file
    form = SQLFORM.factory(Field('fromfile', 'upload'))
    return dict(form=form)

def url(): # get text from url
    form = SQLFORM.factory(Field('urladres')).process()
    if form.accepted:
        session.urladres=request.vars.urladres
        redirect(URL('url_concordance'))
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)

def url_concordance(): # create concordance from web page (get url, returns sorted list)
    text1 = urllib.urlopen(session.urladres).read()
    a = 'windows-1251'
    b = 'utf-8'
    if a in text1:
        text2 = text1.decode('windows-1251')
    elif b in text1:
        text2 = text1.decode('utf-8')
    else:
        text2 = text1.decode('windows-1251')
    text2 = nltk.clean_html(text2)
    normal = normaliz1(tokenize1(text2))
    normal.sort(key = itemgetter(1), reverse = True)
    url_id=test.url.insert(text=text2, urladres=session.urladres, wordfile=normal)
    animals = test().select(test.url.ALL)
    return dict(normal=normal, animals=animals)

def forma():
    forma = test().select(test.morpho.ALL, orderby=test.morpho.id)
    return dict(forma=forma)

def bigram():
    text2 = test(test.text2.id==request.args(0)).select().first()
    text1 = text2['body'].decode('utf-8')
    normal = tokenize1(text1)
    finder = BigramCollocationFinder.from_words(normal)
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    list = sorted(bigram for bigram, score in scored)
#    list=finder.nbest(bigram_measures.pmi, 2)
    return dict(list=list)

def dost():
    texts = test(test.morpho.author == 'Достоевский').select()
    return dict(texts=texts)

def oberiu_pos():
    texts = test(test.morpho.groups=='oberiu').select()
    pos = morphot(morphot.pos.groups == 'oberiu').select()
    return dict(texts=texts, pos=pos)

def pushkin():
    texts = test(test.morpho.author == 'Пушкин').select()
    return dict(texts=texts)

def blok():
    texts = test(test.morpho.author == 'Блок').select()
    pos = morphot(morphot.pos.author == 'Блок').select()
    return dict(texts=texts, pos=pos)

def download():
    return response.download(request, test)

def info():   # считаем статистику текста и сохраняем в базу
    text2 = test(test.text2.id==request.args(0)).select().first()
    text1 = text2['body'].decode('utf-8')
    normal = nltk.wordpunct_tokenize(text1)
    sents = nltk.sent_tokenize(text1)
    sentences = len(sents)
    sr_words = 0
    for s in sents:
        words = nltk.wordpunct_tokenize(s)
        sr_words = len(words) + sr_words
    dlina_predl = float(sr_words)/len(sents)
    dlina_predl = round(dlina_predl, 2)
    summa = 0.0
    quantity = 0
    for words in normal:
        summa = summa + len(words)
        quantity = quantity + 1
    sr_ar=round(summa/quantity, 2)
    normal = normaliz1(tokenize1(text1))
    slovar1 = len(normal)/float(quantity)
    slovar = round(slovar1, 3)
    morpho_id=test.morpho.insert(author=text2.author, title=text2.title, year=text2.year, number=quantity, sr_ar=sr_ar, slovar=slovar, slovoforma=len(normal), sentences=sentences, dlina_predl=dlina_predl)
    return dict(sr_ar=sr_ar, quantity=quantity, text2=text2, sentences=sentences, dlina_predl=dlina_predl, normal=normal, slovar=slovar)

def chast_rechi(): # morphological analysis of unprepared text, returns number of every part of speech
    text2 = test(test.text2.id==request.args(0)).select().first()
    text1 = text2['body'].decode('utf-8')
    text1 = nltk.wordpunct_tokenize(text1)
    stop = [',', '.', ';', ':', '!', '?', '...', '—', '-', '«', '»', '»', '"', '*', '— ', '!».', '!»', '4', '5', '6', '7', '8', '9', '0']
    tokens = [s.lower() for s in text1 if s not in stop]
    morph = pymorphy2.MorphAnalyzer()
    verb = 0.0
    adjf = 0.0
    adjs = 0.0
    infn = 0.0
    noun = 0.0
    sluzh = 0.0
    sl = []
    for w in tokens:
        f = morph.parse(w)[0]
        if f.tag.POS == 'VERB':
            verb = verb+1
        if f.tag.POS == 'ADJF':
            adjf = adjf + 1
        if f.tag.POS == 'ADJS':
            adjs = adjs + 1
        if f.tag.POS == 'INFN':
            infn = infn + 1
        if f.tag.POS == 'NOUN':
            noun = noun + 1
        if f.tag.POS == 'PREP' or f.tag.POS == 'CONJ' or f.tag.POS == 'PRCL':
            sluzh = sluzh + 1
            sl.append(w)
    sr_verb = round(float(verb)/len(tokens), 3)
    sr_adjf = round(float(adjf)/len(tokens), 3)
    sr_adjs = round(float(adjs)/len(tokens), 3)
    sr_infn = round(float(infn)/len(tokens), 3)
    sr_noun = round(float(noun)/len(tokens), 3)
    sr_sluzh = round(float(sluzh)/len(tokens), 3)
    morphot_id=morphot.pos.insert(author=text2.author, title=text2.title, noun=sr_noun, verb=sr_verb, adjf=sr_adjf, adjs=sr_adjs, infn=sr_infn, sluzh=sr_sluzh, year=text2.year)
    return dict(verb=int(verb), sr_verb=sr_verb, adjf=int(adjf), sr_adjf=sr_adjf, adjs=int(adjs), sr_adjs=sr_adjs, infn=int(infn), sr_infn=sr_infn, noun=int(noun), sr_noun=sr_noun, sluzh=int(sluzh), sr_sluzh=sr_sluzh, text2=text2, sl=sl)