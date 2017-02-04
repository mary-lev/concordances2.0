# coding: utf8
# попробовать что-либо вида
import difflib
import re
import gensim

def index():
    return dict(message="hello from zatochnik.py")

def compare():
    variant = trymysql(trymysql.drafts.text==10277).select()
    text = variant[int(request.args(0))]
    variant.exclude(lambda r: r.id == text.id)
    t1 = open(text.filename, 'rb')
    text1 = t1.readlines()
    table = []
    for all in variant:
        result = []
        filename2 = all.filename
        t2 = open(filename2, 'rb')
        text2 = t2.readlines()
        # сравниваем тексты
        for l in text2:
            t = text1[text2.index(l)]
            p = ['(', ')', '[', ']', "’"]
            for all in p:
                t = t.replace(all, '')
                l = l.replace(all, '')
            l = re.findall(ur"\w+[ ]|\w+|[,]|[.]", l.decode('utf-8'), re.U)
            l = [all.replace(' ', '') for all in l]
            t = re.findall(ur"\w+[ ]|\w+|[,]|[.]", t.decode('utf-8'), re.U)
            t = [all.replace(' ', '') for all in t]
            d = difflib.Differ()
            r = list(d.compare(t, l))
            result.append(r)
        table.append(result)
    counts = []
    for result in table:
        plus = 0
        minus = 0
        right = 0
        for r in result:
            for w in r:
                if w.startswith('+'):
                    plus += 1
                elif w.startswith('-'):
                    minus += 1
                elif w.startswith('?') or w.startswith('.'):
                    pass
                else:
                    right += 1
        pr = (right*100)/(right+plus+minus)
        counts.append([right, plus, minus, pr])
    return dict(table=table, text=text, counts = counts)

def table():
    variant = trymysql(trymysql.drafts.text==10277).select()
    text = []
    titles = []
    documents=[]
    for all in variant:
        docs = []
        doc = []
        titles.append(all.title)
        t1 = open(all.filename, 'rb')
        text1 = t1.readlines()
        text.append(text1)
        for l in text1:
            doc = doc + l.split()
        docs = gensim.models.doc2vec.TaggedDocument(words=doc, tags=[all.title])
        documents.append(docs)
    model = gensim.models.doc2vec.Doc2Vec(documents, size=100, window=5, min_count=1, workers=3)
    c = model.docvecs.most_similar(1)
    return dict(text=text, docs = docs, model=model, c=c, titles=titles)
