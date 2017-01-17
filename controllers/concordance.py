# coding: utf8
# coding: utf8
import nltk
import pymorphy2
from operator import itemgetter
import select
import gensim, logging
from gensim import corpora, models, similarities
from gensim.models import doc2vec
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import pickle

partos = ['VERB', 'NOUN', 'ADJF', 'ADJS', 'INFN', 'GRND', 'PRTF', 'PRTS', 'ADVB']

def index(): # concordance of one text
    all_words = trymysql(trymysql.allword.title==request.args(0)).select()
    lens=len(all_words)
    vocab = []
    for row in all_words:
        w = row.word
        q = trymysql((trymysql.allword.word==row.word)&(trymysql.allword.title==request.args(0))).select()
        qq = round(((len(q)/float(lens))*100), 2)
        c = [w, len(q), qq]
        if c not in vocab:
            vocab.append(c)
    vocab.sort(key = itemgetter(0), reverse=False)
    return dict(lens=lens, vocab=vocab)

def create_concordance():
    f = open('/home/concordance/dictionary.txt', 'r')
    words = f.readlines()
    count=len(words)
    return dict(words=words, count=count)

def create_number():
    all_texts=trymysql(trymysql.allword.title<10).select()
    concor=trymysql(trymysql.concordance.id>0).select()
    words_concordance = [one.word for one in concor]
    for all in all_texts:
        if all.word in words_concordance:
            number = trymysql(trymysql.concordance.word==all.word).select()[0]
            number_id=number.id
            all.update_record(concordance_number=number_id)
        else:
            all.update_record(concordance_number=0)
    return dict(words=words_concordance[:10], all_texts=all_texts)

def create_vector():
    all_texts=trymysql(trymysql.text1.id<10).select()
    vector = []
    for all in all_texts:
        numbers = [all.concordance_number for all in trymysql(trymysql.allword.title==all.id).select()]
        vector.append(numbers)
    return dict(vector=vector)

stop = ['сам', 'такой', 'свой', 'этот', 'другой', 'хороший', 'целый', 'весь', 'тот', 'последний', 'мой', 'твой', 'наш', 'раз', 'какой', 'один', 'новый', 'полный', 'тук', 'каждый', 'большой', 'всякий', 'самый']

def word2vec():
    sentences1 = []
    for all in trymysql(trymysql.text1.id>0).select():
        part=['NOUN', 'ADJF']
        one = [alles.word for alles in trymysql((trymysql.allword.title==all.id)&(trymysql.allword.partos.belongs(part))).select() if alles.word not in stop]
        sentences1.append(one)
    model1 = gensim.models.Word2Vec(sentences1, min_count=20, window=30, size=300)
    model1.save("/home/concordance/web2py/applications/test/uploads/models/model_from_10_win2_size300")
    return dict(model1=model1)

def model():
    #new_model = gensim.models.Word2Vec.load("/home/concordance/web2py/applications/test/uploads/models/a_model_from_50_win20_size300")
    new_model = gensim.models.Word2Vec.load("/home/concordance/web2py/applications/test/uploads/models/model_from_10_win2_size300")
    #new_model = gensim.models.Word2Vec.load('/home/concordance/deposit/model3')
    words = ['город', 'конь', 'сон', 'огонь', 'мир', 'море', 'день', 'дом', 'ночь']
    words = [all.decode('utf-8') for all in words]
    return dict(model1=new_model, words=words)

def ask_model():
    form = SQLFORM.factory(Field('first', label=T('Слово'))).process()
    if form.accepted:
        redirect(URL('resp_model', vars = form.vars))
    return dict(form=form)

def resp_model():
    model = gensim.models.Word2Vec.load("/home/concordance/web2py/applications/test/uploads/models/model_from_10_win2_size300")
    model1 = gensim.models.Word2Vec.load('/home/concordance/deposit/model10t_20_15')
    model2 = gensim.models.Word2Vec.load('/home/concordance/web2py/applications/test/uploads/models/xx_stemmed_10_10_300')
    words = request.vars.first
    return dict(model=model, words=words, model1=model1, model2=model2)

def doc2vec():
    documents = []
    authors = [1, 2, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    #authors = [1,5]
    titles = [all.id for all in trymysql(trymysql.text1.id>0).select()]
    part=['ADJF', 'NOUN', 'VERB']
    for all in titles:
        one = [alles.word for alles in trymysql((trymysql.allword.title==all)&(trymysql.allword.partos.belongs(part))).select()]
        docs = gensim.models.doc2vec.TaggedDocument(words=one, tags=[all])
        documents.append(docs)
    model = gensim.models.doc2vec.Doc2Vec(documents, size=100, window=8, min_count=5, workers=4)
    model.save("/home/concordance/web2py/applications/test/uploads/models/allpoets")
    c = model.docvecs.most_similar(1)
    docs = []
    for all in c:
        text = trymysql(trymysql.text1.id==all[0]).select()[0]
        docs.append(text)
    osn = trymysql(trymysql.text1.id==1).select()[0]
    return dict(documents=c, docs= docs, osn=osn)

def doc2vec_find():
    poem = int(request.vars.first)
    model = gensim.models.doc2vec.Doc2Vec.load("/home/concordance/web2py/applications/test/uploads/models/allpoets")
    c = model.docvecs.most_similar(poem)

    docs = []
    nn = []
    for all in c:
        text = trymysql(trymysql.text1.id==all[0]).select()[0]
        #n = model.docvecs.n_similarity(request.vars.first, all[0]))
        docs.append(text)
        #nn.append(n)
    osn = trymysql(trymysql.text1.id==poem).select()[0]
    return dict(documents=c, docs=docs, osn=osn)

def doc2vec_load():
    form = SQLFORM.factory(Field('first')).process()
    if form.accepted:
        redirect(URL('doc2vec_find', vars = form.vars))
    return dict(form=form)

def couple_form():
    form = SQLFORM.factory(Field('first'), Field('second')).process()
    if form.accepted:
        redirect(URL('couple', vars = form.vars))
    return dict(form=form)

def couple():
    title = []
    first = [all.title for all in trymysql(trymysql.allword.word==request.vars.first).select()]
    for all in first:
        if len(trymysql((trymysql.allword.word == request.vars.second)&(trymysql.allword.title==all)).select()) > 0:
            title.append(all)
    title = sorted(set(title))
    texts = trymysql(trymysql.text1.id.belongs(title)).select()
    return dict(title=title, one = request.vars.first, two = request.vars.second, texts=texts)

def test_gensim():
    alles = []
    for all in trymysql(trymysql.text1.id>0).select():
        one=[new.word for new in trymysql((trymysql.allword.title==all.id)&(trymysql.allword.partos=="NOUN")).select()]
        alles.append(one)
    dictionary = gensim.corpora.Dictionary(alles)
    corpus = [dictionary.doc2bow(alle) for alle in alles]
    tfidf = models.TfidfModel(corpus, id2word=dictionary)
    corpus_tfidf = tfidf[corpus]
    #lsi = models.lsimodel.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=5)
    lda = gensim.models.ldamodel.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=15, update_every=1, chunksize=10000, passes=1)
    #topics=lsi.print_topics(15)
    topics=lda.print_topics(20)
    return dict(topics=topics)

def birds():
    new_model = gensim.models.Word2Vec.load("/home/concordance/web2py/applications/test/uploads/models/model_from_10_win2_size300")
    return dict(model1=new_model)

def zveri():
    new_model = gensim.models.Word2Vec.load("/home/concordance/web2py/applications/test/uploads/models/model_from_10_win2_size300")
    words = ['волк', 'зверь', 'конь', 'лошадь', 'мышь', 'пёс', 'собака']
    words = [all.decode('utf-8') for all in words]
    return dict(model1=new_model, words=words)

def conc(): #самые употребляемые слова (от 500)
    count = trymysql.allword.id.count()
    words = []
    for row in trymysql(trymysql.allword.id>0).select(trymysql.allword.word, count, groupby=trymysql.allword.word):
        if row[count] >500:
            words.append([row.allword.word, row[count]])
    words.sort(key = itemgetter(1), reverse=True)

    return dict(words=words)

def save_words():
    sentences1 = []
    part=['NOUN', 'ADJF']
    for all in trymysql(trymysql.text1.id>0).select():
        #sentences1.append([alles.word for alles in trymysql((trymysql.allword.title==all.id)&(trymysql.allword.partos.belongs(part))).select() if alles.word not in stop])
        words = trymysql(trymysql.allword.title==all.id).select(trymysql.allword.word)
        l = [all.word for all in words if all.word not in stop]
        sentences1.append(l)
    #model1 = gensim.models.Word2Vec(sentences1, min_count=20, window=15, size=300)
    #model1.save("/home/concordance/web2py/applications/test/uploads/models/all_model_from_20_win15_size300")
    words = [all.word for all in trymysql((trymysql.allword.title=='1000L')&(trymysql.allword.partos.belongs(part))).select(trymysql.allword.word)]
    with open('/home/concordance/web2py/applications/test/uploads/models/all_partos.txt', 'wb') as f:
        pickle.dump(sentences1, f)
    return dict(model1=len(sentences1), w=words)
