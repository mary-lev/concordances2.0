# coding: utf8
# попробовать что-либо вида
def index():
    dates = trymysql(trymysql.text1.day_writing>0).select()
    return dict(dates=dates)