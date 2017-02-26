# coding: utf8
# попробовать что-либо вида

def index():
    dates = trymysql(trymysql.text1.year_writing=='1900').select()
    return dict(dates=dates)

def year():
    new_year = request.args(0)
    dates = trymysql((trymysql.text1.day_writing>0)&(trymysql.text1.year_writing==new_year)).select()
    return dict(new_year=new_year, dates=dates)

def update_dates():
    dates = trymysql((trymysql.text1.id==7632)&(trymysql.text1.author==19)).select()
    #dates = [all.year_writing for all in dates]
    n = []
    for all in dates:
        a = all.year_writing[:-1]
        b = all.month_writing[:-1]
        c = all.day_writing[:-1]
        all.update_record(year_writing=a, month_writing = b, day_writing=c)
    return dict(dates=a)
