#!/usr/bin/env python
# coding: utf8
from gluon import *
from gluon import current

def au():
    trymysql = current.globalenv['trymysql']
    a = trymysql(trymysql.author.id>0).select()
    return a
