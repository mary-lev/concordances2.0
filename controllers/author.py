# coding: utf8

def index():
    authors = trymysql().select(trymysql.author.ALL, orderby=trymysql.author.id)
    return dict(authors=authors)

def all_author():
    texts=trymysql(trymysql.text1.author==request.args(0)).select()
    author= trymysql(trymysql.author.id==request.args(0)).select()[0]
    return dict(texts=texts, author=author)

def years():
    all_years = [int(all.year_writing) for all in trymysql().select(trymysql.text1.ALL) if all.year_writing]
    year=[]
    year_sorted=sorted(set(all_years))
    for x in year_sorted:
        year_writing = trymysql((trymysql.text1.year_writing==x)&(trymysql.text1.author==request.args(0))).count()
        year.append((x, year_writing))
    month = [(x, trymysql(trymysql.text1.month_writing==x).count()) for x in range(1,13)]
    return dict(year=year, year_sorted=year_sorted, month=month)
