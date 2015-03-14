# coding: utf8
from operator import itemgetter

def index():
    authors = trymysql().select(trymysql.author.ALL, orderby=trymysql.author.id)
    return dict(authors=authors)

def count_all():
    texts = trymysql(trymysql.text1.author==request.args(0)).select()
    author1=trymysql(trymysql.author.id==request.args(0)).select().first()
    return dict(texts=texts, author1=author1)

def count_partos():
    part = ['NOUN', 'ADJF', 'ADJS', 'VERB', 'INFN', 'GRND', 'PRTF', 'PRTS', 'ADVB', 'PREP', 'CONJ', 'NPRO', 'PRCL' ]
    parts=[trymysql((trymysql.allword.partos==all)&(trymysql.allword.author==request.args(0))).count() for all in part]
    author1=trymysql(trymysql.author.id==request.args(0)).select()[0]
    author=author1['family']
    return dict(parts=parts, author=author)

def count_concordance():
    texts = trymysql(trymysql.allword.partos=='NOUN').select()
    c = len(texts)
    words=[all['word'] for all in texts]
    words1 = [(word, words.count(word)) for word in words]
    words1=sorted(set(words1))
    words1.sort(key = itemgetter(1), reverse = True)
    return dict(c=c, words1=words1)

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
    words1 = trymysql((trymysql.allword.author==request.args(0))&(trymysql.allword.partos!='None')&(trymysql.allword.partos!="PNCT")).select()
    words = [all.word for all in words1]
    lemmas_sort = sorted(set(words))
    w_range = float(len(lemmas_sort)/(len(words)*1.0))
    return dict(w_range=w_range)

def test_bar():
    authors = trymysql(trymysql.text1.author=='1').select()
    years = [all.year_writing for all in authors]
    words1 = [(all, years.count(all)) for all in years]
    words1=sorted(set(words1))
    new_author = trymysql(trymysql.text1.author=='5').select()
    years2 = [all.year_writing for all in new_author]
    words2 = [(all, years2.count(all)) for all in years2]
    words2 = sorted(set(words2))
    return dict(words1=words1, words2=words2)
