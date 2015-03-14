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
