#!/usr/bin/env python
# coding: utf8
from gluon import *
import nltk
import pymorphy2
from operator import itemgetter

def tokenize1(text1): # tokenization of decoded text, returns list of tokens
    text3 = nltk.wordpunct_tokenize(text1)
    stop = [',', '.', ';', ':', '!', '?', '!"', '..', '!.', '...', '—', '-', '«', '»', '»', '"', '— ', '—', '!».', '!»', '4', '5', '6', '7', '8', '9', '0']
    tokens = [s.lower() for s in text3 if s not in stop]
    return tokens

def normaliz1(tokens): # get tokens and return list of normal forms with quantity of usage and term frequency
    morph = pymorphy2.MorphAnalyzer()
    normal = []
    listx = []
    sr_ar = 0.0
    normal_all = [morph.parse(w)[0].normal_form for w in tokens]
    for w in normal_all:
        if w not in listx:
            number = normal_all.count(w)
            sr_ar = float(number)/len(normal_all)*100
            sr_ar=round(sr_ar, 3)
            normal.append([w, number, sr_ar])
            listx.append(w)
        else:
            pass
    return normal

def normalize_new(text1): # get tokens and return list of normal forms with quantity of usage and term frequency (for /control/...)
    text3 = nltk.wordpunct_tokenize(text1)
    stop = [',', '.', ';', ':', '!', '!..', '?', '...', '—', '-', '«', '»', '»', '"', '— ', '—', '!».', '!»', '4', '5', '6', '7', '8', '9', '0']
    tokens = [s.lower() for s in text3 if s not in stop]
    morph = pymorphy2.MorphAnalyzer()
    normal = []
    for w in tokens:
        p = morph.parse(w)[0]
        lemma = p.normal_form
        partos = p.tag.POS
        normal.append([lemma, partos, w])
    else:
        pass
    return normal

def normalize_new2(text1):
    text3 = nltk.wordpunct_tokenize(text1)
    morph = pymorphy2.MorphAnalyzer()
    normal = []
    count=0
    for w in text3:
        p = morph.parse(w)[0]
        normal.append([p.normal_form, p.tag.POS, w, count, p.tag.tense])
        count +=1
    else:
        pass
    return normal

def normalize_save_partos(text1):
    text3 = nltk.wordpunct_tokenize(text1)
    morph = pymorphy2.MorphAnalyzer()
    normal = []
    count=0
    for w in text3:
        p = morph.parse(w)[0]
        normal.append([p.normal_form, p.tag.POS, w, count, p.tag.tense])
        count +=1
    else:
        pass
    return normal
def verbalize1(tokens): # get tokens and return top-10 of verbs
    morph = pymorphy2.MorphAnalyzer()
    list_verb=[]
    verb=[]
    normal_all = [morph.parse(w)[0].normal_form for w in tokens]
    for w in normal_all:
        if w not in list_verb:
            f = morph.parse(w)[0]
            if f.tag.POS == 'INFN':
                number = normal_all.count(w)
                sr_ar = float(number)/len(normal_all)*100
                verb.append([w, number])
                list_verb.append(w)
            else:
                pass
        else:
            pass
    verbs_lemmas=[n[0].encode('utf-8') for n in verb]
    verb.sort(key = itemgetter(1), reverse = True)
    top_verbs=verb[:10]
    return top_verbs
