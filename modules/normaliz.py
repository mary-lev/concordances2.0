#!/usr/bin/env python
# coding: utf8
from gluon import *
import pymorphy2

# normalization of the list of tokens, returns not sorted list of normal forms with weight of every form

class Text6():

    def __init__(tokens):
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
