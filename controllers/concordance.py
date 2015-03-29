# coding: utf8
# coding: utf8
import nltk
import pymorphy2
from operator import itemgetter
import select
from gensim import corpora, models, similarities
import gensim, logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

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
    all_words = trymysql().select(trymysql.allword.ALL)
    all1=[all.word for all in all_words if all.partos in partos]
    words=sorted(set(all1))
    for token in words:
            trymysql.concordance.insert(word=token)
    return dict(words=words)

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

def word2vec():
    part=['NOUN', 'ADJF', 'VERB']
    sentences = []
    sentences1 = []
    for all in trymysql(trymysql.text1.author==5).select():
        # one = [all.word for all in trymysql((trymysql.allword.title==all.id)&(trymysql.allword.partos.belongs(part))).select()]
        one = [all.word for all in trymysql((trymysql.allword.title==all.id)&(trymysql.allword.partos.belongs(part))).select()]
        sentences.append(one)
    for all in trymysql(trymysql.text1.author==1).select():
        part=['NOUN', 'ADJF']
        # one = [all.word for all in trymysql((trymysql.allword.title==all.id)&(trymysql.allword.partos.belongs(part))).select()]
        one = [all.word for all in trymysql((trymysql.allword.title==all.id)&(trymysql.allword.partos.belongs(part))).select()]
        sentences1.append(one)
    model = gensim.models.Word2Vec(sentences, min_count=5, size=25)
    model1 = gensim.models.Word2Vec(sentences1, min_count=5, size=25)
    return dict(model=model, model1=model1)

def test_gensim():
    alles = []
    for all in trymysql(trymysql.text1.id>0).select():
        one=[new.word for new in trymysql((trymysql.allword.title==all.id)&(trymysql.allword.partos.belongs(("NOUN", "VERB")))).select()]
        alles.append(one)
    dictionary = gensim.corpora.Dictionary(alles)
    corpus = [dictionary.doc2bow(alle) for alle in alles]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=15)
    #lda = gensim.models.ldamodel.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=15, update_every=1, chunksize=10000, passes=1)
    topics=lsi.print_topics(15)
    return dict(topics=topics)
