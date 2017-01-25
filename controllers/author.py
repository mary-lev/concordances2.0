# coding: utf8
import numpy as np

def index():
    authors = trymysql().select(trymysql.author.ALL, orderby=trymysql.author.id)
    return dict(authors=authors)

def all_author():
    texts=trymysql(trymysql.text1.author==request.args(0)).select() # orderby=trymysql.text1.title|trymysql.text1.first_string
    books = trymysql(trymysql.group_text.author==request.args(0)).select(groupby=trymysql.group_text.id)
    variants = [all.text for all in trymysql(trymysql.drafts.author==request.args(0)).select()]
    book = [all.book for all in trymysql((trymysql.drafts.text.belongs(variants))&(trymysql.drafts.author==request.args(0))).select(trymysql.drafts.book, groupby=trymysql.drafts.book)]
    publ = trymysql((trymysql.biblio.id.belongs(book))&(trymysql.biblio.year!='')).select(orderby=trymysql.biblio.year)
    return dict(texts=texts, variants=variants, publ=publ, books=books)

def years():
    all_years = [int(all.year_writing) for all in trymysql().select(trymysql.text1.ALL) if all.year_writing]
    year=[]
    year_sorted=sorted(set(all_years))
    for x in year_sorted:
        year_writing = trymysql((trymysql.text1.year_writing==x)&(trymysql.text1.author==request.args(0))).count()
        year.append((x, year_writing))
    month = [(x, trymysql(trymysql.text1.month_writing==x).count()) for x in range(1,13)]
    author = trymysql(trymysql.author.id==request.args(0)).select()[0]
    name = author.family
    return dict(year=year, year_sorted=year_sorted, month=month, name=name)

def text():
    l = []
    stroka = []
    words = []
    for all in trymysql(trymysql.text1.author==request.args(0)).select():
        f = open(all.filename, 'rb')
        content = f.readlines()
        l.append(len(content))
        for all in content:
            stroka.append(len(all))
            words.append(len(all.split()))
    res = np.mean(l)
    stroka=np.mean(stroka)
    words = np.mean(words)
    res_m = np.median(l)
    author = trymysql(trymysql.author.id==request.args(0)).select()[0]
    name = author.family
    return dict(res=res, stroka=stroka, words=words, res_m = res_m, name=name)
