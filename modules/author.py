#!/usr/bin/env python
# coding: utf8
from gluon import *

def au():
    a = trymysql(trymysql.author.id>0).select()
    return a