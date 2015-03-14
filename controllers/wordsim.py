# coding: utf8

color=["день", "ночь", "утро", "вечер", "сумерки", "рассвет", "заря", "дневной", "утренний", "вечерний", "ночной", "дневной", "земля", "небо", "лес"]
colors1 = color
def index():
    numbers=[]
    lists=[]
    for each in color:
        list1=[int(all.title) for all in trymysql((trymysql.allword.word==each)&(trymysql.allword.author==9)).select()]
        numbers.append(sorted(set(list1)))
    for all in numbers:
        lists.append([len(trymysql((trymysql.allword.title.belongs(all))&(trymysql.allword.word==every)).select(groupby=trymysql.allword.title)) for every in colors1])
    newnew=[]
    for all in lists:
        newlist=[]
        for each in all:
            if lists.index(all) == all.index(each):
                each = 0
            newlist.append(each)
        newnew.append(newlist)
    return dict(lists=lists, color=color, newnew=newnew)
