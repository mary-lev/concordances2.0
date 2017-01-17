# coding: utf8
# попробовать что-либо вида
import nltk

def index():
    return dict(message="hello from scikit.py")

def docs():
    documents = [1,2,3,4,5]
    featuresets = [(document_features(d), 'pos') for d in documents]
    train_set, test_set = featuresets[100:], featuresets[:100]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    t = nltk.classify.accuracy(classifier, test_set)
    return dict(t=t)

def document_features(document):
    f = open('/home/concordance/dictionary.txt', 'r')
    words = f.readlines()
    word_features = [all.split()[0] for all in words[:2000]]
    features = {}
    doc_words = [row.word for row in trymysql(trymysql.allword.title==int(document)).select()]
    document_words = set(doc_words)
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return dict(features=features)

def pos():
    author_texts = [all.id for all in trymysql(trymysql.text1.author==n).select()]
    count = trymysql.allword.id.count()
    words = []
    for row in trymysql(trymysql.allword.pos=='NOUN').select(trymysql.allword.word, count, groupby=trymysql.allword.word):
        if row[count] >500:
            words.append([row.allword.word, row[count]])
    words.sort(key = itemgetter(1), reverse=True)
