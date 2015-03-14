# coding: utf8
from operator import itemgetter

color=["зелёный", "золотой", "голубой", "красный", "белый", "жёлтый", "чёрный", "коричневый", "синий", "розовый", "пурпурный", "фиолетовый", "серый", "лазурный", "алый"]
colors1 = color
def index():
    return dict()

def index1(): # count correlation between colors in texts
    numbers=[]
    lists=[]
    for each in color:
        list1=[int(all.title) for all in trymysql((trymysql.allword.word==each)&(trymysql.allword.author==1)).select()]
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

def index2(): # search for similar texts in corpus (similarity for list of words)
    parts = ['NOUN', 'VERB', 'INFN', 'ADJF', 'ADJS']
    old = request.args(0)
    words = [all.word for all in trymysql((trymysql.allword.title==request.args(0))&(trymysql.allword.partos.belongs(parts))).select()]
    selected = trymysql(trymysql.text1.id==request.args(0)).select()[0]
    author = trymysql(trymysql.author.id==int(selected.author)).select()[0]
    words = sorted(set(words))
    titles = [all.title for all in trymysql(trymysql.allword.word.belongs(words)).select()]
    titles=sorted(set(titles))
    quantity = []
    max_score=[]
    for every in titles:
        number = [len(trymysql((trymysql.allword.title==every)&(trymysql.allword.word==new)).select()) for new in words if len(trymysql((trymysql.allword.title==every)&(trymysql.allword.word==new)).select())!=0]
        quantity.append((every, len(number)))
        max_score.append(len(number))
    quantity.sort(key = itemgetter(1), reverse=True)
    max_score=sorted(set(max_score))[-4]
    relevant = [all[0] for all in quantity if all[1]>max_score]
    relevant_list = trymysql(trymysql.text1.id.belongs(relevant)).select()
    return dict(words=words, relevant=relevant, relevant_list=relevant_list, author=author.family, selected=selected, max_score=max_score, old=old)

def compare(): # Сравниваем лексику двух текстов
    text1=trymysql(trymysql.allword.title==request.args(0)).select()
    text1_info = trymysql(trymysql.text1.id==request.args(0)).select()[0]
    text2=trymysql(trymysql.allword.title==request.args(1)).select()
    text2_info = trymysql(trymysql.text1.id==request.args(1)).select()[0]
    lemmas1 = [all.word for all in text1]
    lemmas2=[all.word for all in text2]
    result= sorted(set(lemmas1) - set(lemmas2))
    result2= sorted(set(lemmas2) - set(lemmas1))
    l1 = len(lemmas1)
    l2 = len(lemmas2)
    all = len(lemmas1) - len(result)
    return dict(result=result, result2=result2, l1=l1, l2=l2, all=all, text1=text1, text2=text2, text1_info=text1_info, text2_info=text2_info)

def index3(): # draft: search for similar texts in corpus (similarity for list of words)
    parts = ['NOUN', 'VERB', 'INFN', 'ADJF', 'ADJS']
    words = [all.word for all in trymysql((trymysql.allword.title==request.args(0))&(trymysql.allword.partos.belongs(parts))).select()]
    selected = trymysql(trymysql.allword.title==request.args(0)).select()[0]
    sq = selected.author
    author = trymysql(trymysql.author.id==int(sq)).select()[0]
    words = sorted(set(words))
    titles = [all.title for all in trymysql(trymysql.allword.word.belongs(words)).select()]
    titles=sorted(set(titles))
    summary = [[each, trymysql((trymysql.allword.word.belongs(words))&(trymysql.allword.title==each)).count()] for each in titles] # в абсолютных цифрах
    quantity = []
    for every in titles:
        number = [len(trymysql((trymysql.allword.title==every)&(trymysql.allword.word==new)).select()) for new in words if len(trymysql((trymysql.allword.title==every)&(trymysql.allword.word==new)).select())!=0]
        quantity.append((every, len(number)))
        max_score.append(len(number))
    quantity.sort(key = itemgetter(1), reverse=True)
#    summary1 = [[each, (trymysql((trymysql.allword.word.belongs(words))&(trymysql.allword.title==each)).count()*1.0)/trymysql(trymysql.allword.title==each).count()] for each in titles] # в процентах
    summary.sort(key = itemgetter(1), reverse=True)
#    summary1.sort(key = itemgetter(1), reverse=True)
    best = [all[0] for all in summary[:6]]
#    best1 = [all[0] for all in summary1[:6]]
    relevant = [(row.title, row.author) for row in trymysql(trymysql.text1.id.belongs(best)).select()]
#    relevant1 = [row.title for row in trymysql(trymysql.text1.id.belongs(best1)).select()]
    return dict(words=words, data = summary[:6], relevant=relevant, best=best, author=author.family, quantity=quantity)
