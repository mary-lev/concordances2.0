# coding: utf8
import gensim, logging
from gensim import corpora, models, similarities
from gensim.models import doc2vec
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import Levenshtein
from operator import itemgetter
from scipy.cluster.vq import kmeans
import numpy as np


def index():
    string1 = trymysql(trymysql.text1.id==516).select()[0]
    drafts = []
    for all in trymysql(trymysql.drafts.id>0).select():
        with open(all.filename, 'r') as f:
            first = f.readlines()
        string2 = ' '.join(first)
        distance = Levenshtein.distance(string1.body, string2)
        drafts.append([distance, all.id])
    drafts.sort(key = itemgetter(0), reverse=False)
    drafts_list = [all[0] for all in drafts]
    poems = []
    for all in drafts[:10]:
        poems.append(trymysql(trymysql.drafts.id==all[1]).select()[0])
    return dict(drafts=drafts, string1=string1, poems=poems)

def find_similar():
    string = trymysql(trymysql.text1.id==request.args(0)).select()[0]
    other = []
    for all in trymysql(trymysql.text1.author==string.author).select():
        with open(all.filename, 'r') as f:
            first = f.readlines()
        string2 = ' '.join(first)
        distance = Levenshtein.distance(string.body, string2)
        other.append([distance, all.id])
    other.sort(key = itemgetter(0), reverse=False)
    poems = []
    for all in other[:10]:
        poems.append(trymysql(trymysql.text1.id==all[1]).select()[0])
    return dict(other=other, string=string, poems=poems)
