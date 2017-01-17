# coding: utf8
from operator import itemgetter

partos = ['NOUN', 'ADJF', 'ADJS', 'VERB', 'INFN', 'GRND', 'PRTF', 'PRTS', 'ADVB', 'PREP', 'CONJ', 'NPRO', 'PRCL' ]

def index():
    authors = trymysql().select(trymysql.author.ALL, orderby=trymysql.author.family)
    return dict(authors=authors)

def count_partos():
    part = ['NOUN', 'ADJF', 'ADJS', 'VERB', 'INFN', 'GRND', 'PRTF', 'PRTS', 'ADVB', 'PREP', 'CONJ', 'NPRO', 'PRCL' ]
    parts=[trymysql((trymysql.allword.partos==all)&(trymysql.allword.author==request.args(0))).count() for all in part]
    author1=trymysql(trymysql.author.id==request.args(0)).select()[0]
    author=author1['family']
    return dict(parts=parts, author=author)

def count_concordance():
    for all in trymysql((trymysql.concordance.id>13500)&(trymysql.concordance.id<14500)).select():
        summa = trymysql((trymysql.allword.word==all.word)&(trymysql.allword.partos=='NOUN')).count()
        all.update_record(number=int(summa))
    #words1=sorted(set(words1))
    #words1.sort(key = itemgetter(1), reverse = True)
    new=[all.word for all in trymysql(trymysql.concordance.number>500).select()]
    t = type(trymysql(trymysql.concordance.id==100).select()[0].number)
    return dict(new=new, t=t)

def sentence_len(): # count mean of length of centences of the author
    texts = trymysql(trymysql.allword.author==request.args(0)).select()
    part = ['.', '!', '...', '?']
    points = trymysql((trymysql.allword.author==request.args(0))&(trymysql.allword.word.belongs(part))).count()
    words = trymysql(trymysql.allword.author==request.args(0)).count()
    sentence=float(words/(points*1.0))
    return dict(sentence=sentence)

def words_len(): # count mean of length of all words of the author and draw a distribution histogram
    texts = trymysql((trymysql.allword.author==request.args(0))&(trymysql.allword.partos!='None')&(trymysql.allword.partos!="PNCT")).select()
    list_lemma = [len(all.lemma.decode('utf-8')) for all in texts]
    distribution = sorted(set([(all, list_lemma.count(all)) for all in list_lemma]))
    words_length = round(sum(list_lemma)/(len(texts)*1.0), 3)
    return dict(words_length=words_length, distribution=distribution)

def words_range(): # count variety of dictionary of the author
    words = [all.word for all in trymysql((trymysql.allword.author==request.args(0))&(trymysql.allword.partos!='None')&(trymysql.allword.partos!="PNCT")).select()]
    lemmas_sort = sorted(set(words))
    w_range = float(len(lemmas_sort)/(len(words)*1.0))
    return dict(w_range=w_range)

punct = ['.', ',', '!', '?', '—']

def table_data():
    all_words = trymysql(trymysql.allword.author==request.args(0)).count()
    all_texts = trymysql(trymysql.text1.author==request.args(0)).count()
    data = []
    for all in partos:
        words = trymysql((trymysql.allword.author==request.args(0))&(trymysql.allword.partos==all)).count()
        data.append(words)
    pun = []
    all_pun = trymysql((trymysql.allword.author==request.args(0))&(trymysql.allword.word.belongs(punct))).count()
    for all in punct:
        words = trymysql((trymysql.allword.author==request.args(0))&(trymysql.allword.word==all)).count()
        pun.append(words)
    # length of words
    words = [all.lemma for all in trymysql((trymysql.allword.author==request.args(0))&(trymysql.allword.partos.belongs(partos))).select()]
    len_words = 0
    for all in words:
        len_words = len_words+len(all)
    lw = len_words/len(words)
    inan = trymysql(trymysql.allword.anim=='inan').count()
    anim = trymysql(trymysql.allword.anim=='anim').count()
    masc = trymysql(trymysql.allword.gendr=='masc').count()
    femn = trymysql(trymysql.allword.gendr=='femn').count()
    past = trymysql(trymysql.allword.tense=='past').count()
    pres = trymysql(trymysql.allword.tense=='pres').count()
    futr = trymysql(trymysql.allword.tense=='futr').count()
    name = trymysql(trymysql.allword.sobstv!='None').count()
    return dict(data=data, all_words=all_words, all_texts=all_texts, pun = pun, all_pun=all_pun, lw=lw, inan=inan, anim=anim, masc=masc, femn=femn, past=past, pres=pres, futr=futr, name=name)
