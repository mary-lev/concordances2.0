# coding: utf8
# попробовать что-либо вида
import difflib
import re
import gensim
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.manifold import MDS
import pandas as pd

def index():
    texts = trymysql(trymysql.drafts.text==10277).select()
    return dict(texts=texts)

def compare():
    variant = trymysql(trymysql.drafts.text==10277).select()
    text = trymysql(trymysql.drafts.id==request.args(0)).select()[0]
    variant.exclude(lambda r: r.title == text.title)
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
            if request.args(1)=='0':
                l = clear1(l).split()
                t = clear1(t).split()
            elif request.args(1)=='1':
                l = clear(l).split()
                t = clear(t).split()
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

p = ['(', ')', '[', ']', "’", '.', ',', 'I', 'V', 'X', 'L']

def clear(line):
    for all in p:
        line = line.replace(all, '')
    for w in orf:
        line = line.replace(w[0], w[1])
    line = re.findall(ur"\w+[ ]|\w+|[,]|[.]", line.decode('utf-8'), re.U)
    line = [all.replace(' ', '') for all in line]
    line = [w.lower() for w in line]
    return ' '.join(line)

def clear1(line):
    for all in p:
        line = line.replace(all, '')
    line = re.findall(ur"\w+[ ]|\w+|[,]|[.]", line.decode('utf-8'), re.U)
    line = [all.replace(' ', '') for all in line]
    return ' '.join(line)

def line_table():
    variants = trymysql(trymysql.drafts.text==10277).select()
    texts = []
    for all in variants:
        with open(all.filename, 'rb') as f:
            text = f.readlines()
        texts.append(text)
    return dict(texts=texts)

def table():
    variant = trymysql(trymysql.drafts.text==10277).select()
    text = []
    base = trymysql(trymysql.drafts.id==request.args(0)).select()[0]
    t1 = open(base.filename, 'rb')
    text1 = t1.readlines()
    if request.args(1)=='0':
        text1 = [clear(w) for w in text1]
    variant.exclude(lambda r: r.id == request.args(0))
    ids = [all.id for all in variant]
    for all in variant:
        t1 = open(all.filename, 'rb')
        t1 = t1.readlines()
        if request.args(1)=='0':
            t1 = [clear(w) for w in t1]
        text.append(t1)
    return dict(text=text, text1=text1, base=base)

orf = [['ѧ', 'я'], ['і', 'и'], ['i', 'и'], ['ъ', ''], ['ѫ', 'y'], ['ѣ', 'е'], ['оу', 'у'], ['ь', ''], ['ω', 'о'], ['ѕ', 'з'], ['ψ', 'пс'] ]

def word2vec():
    variant = trymysql(trymysql.drafts.text==10277).select()
    text = []
    titles = []
    documents=[]
    docs2 = []
    titls = []
    for all in variant:
        doc = []
        titles.append(all.title)
        titls.append(all.book_page)
        t1 = open(all.filename, 'rb')
        text1 = t1.readlines()
        text.append(text1)
        if request.args(0)=='0':
            for l in text1:
                doc = doc+l.split()
        elif request.args(0)=='1':
            for l in text1:
                doc = doc + clear(l).split()
        docs = gensim.models.doc2vec.TaggedDocument(words=doc, tags=[all.title])
        documents.append(docs)
        docs2.append(' '.join(doc))
    model = gensim.models.doc2vec.Doc2Vec(documents, size=100, window=5, min_count=1, workers=3)
    c = model.docvecs.most_similar(1)
    tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, use_idf=True, ngram_range=(1,3))
    tfidf_matrix = tfidf_vectorizer.fit_transform(docs2) #fit the vectorizer to synopses

    m = tfidf_matrix.shape
    terms = tfidf_vectorizer.get_feature_names()
    dist = 1 - cosine_similarity(tfidf_matrix)
    num_clusters = 4
    km = KMeans(n_clusters=num_clusters)
    km.fit(tfidf_matrix)
    clusters = km.labels_.tolist()
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    pos = mds.fit_transform(dist)  # shape (n_components, n_samples)
    xs, ys = pos[:, 0], pos[:, 1]
    df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=titls))
    groups = df.groupby('label')
    # set up plot
    fig, ax = plt.subplots(figsize=(10, 6)) # set size
    ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling

#iterate through groups to layer the plot
#note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, mec='none')
        ax.set_aspect('auto')
        ax.tick_params(\
                       axis= 'x',          # changes apply to the x-axis
                       which='both',      # both major and minor ticks are affected
                       bottom='off',      # ticks along the bottom edge are off
                       top='off',         # ticks along the top edge are off
                       labelbottom='off')
        ax.tick_params(\
                       axis= 'y',         # changes apply to the y-axis
                       which='both',      # both major and minor ticks are affected
                       left='off',      # ticks along the bottom edge are off
                       top='off',         # ticks along the top edge are off
                       labelleft='off')

    ax.legend(numpoints=1)  #show legend with only 1 point

    #add label in x,y position with the label as the film title
    for i in range(len(df)):
        ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], size=8)
    i = 'plot' + request.args(0) + '.png'
    f = '/home/concordance/web2py/applications/test/static/' + i
    plt.savefig(f) #show the plot

    return dict(model=model, titles=titles, i=i)
