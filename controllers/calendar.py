# coding: utf8
# попробовать что-либо вида

def index():
    dates = trymysql(trymysql.text1.day_writing>0).select()
    return dict(dates=dates)

def year():
    new_year = request.args(0)
    dates = trymysql((trymysql.text1.day_writing>0)&(trymysql.text1.year_writing==new_year)).select()
    return dict(new_year=new_year, dates=dates)
