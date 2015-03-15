# coding: utf8
import nltk
import pymorphy2
from tokenize1 import *
import os
from os import listdir
from os.path import isfile, join
from operator import itemgetter
import subprocess
import select
from lxml import etree
from gensim import corpora, models, similarities
from plugin_sqleditable.editable import SQLEDITABLE
SQLEDITABLE.init()

def index():
    texts = trymysql().select(trymysql.author.ALL, orderby=trymysql.author.family)
    return dict(texts=texts)

def all_texts():
    texts = trymysql().select(trymysql.text1.ALL, orderby=trymysql.text1.id)
    return dict(texts=texts)

def show1():   # show text from file
    texts = trymysql(trymysql.text1.id==request.args(0)).select().first()
    f = open(texts.filename, 'rb')
    content = f.readlines()
    return dict(texts=texts, content=content)

def show2(): # color the verbs
    words = trymysql(trymysql.allword.title==request.args(0)).select()
    content = []
    for row in words:
        if row.partos=='VERB':
            new_words=str(row.lemma)+str('&')
            content.append(new_words)
        else:
            content.append(row.lemma)
    return dict(content=content)

def show3():
    texts = trymysql(trymysql.text1.id==request.args(0)).select().first()
    rows = trymysql(trymysql.allword.title==request.args(0)).select()
    text_view = []
    for row in rows:
        text_view.append((row.lemma, row.id))
    options = [OPTION(row.lemma, _value=row.id) for row in rows]
    form=FORM(TABLE(TR("Выберите текст"),
                    TR("Например, так:",SELECT(*options, _name="first")),
                    TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.accepts(request,session):
        response.flash="form accepted"
    return dict(text_view=text_view, form=form)

def tokenize_all(): # prepares text for tokenization (decoding) and write result in database trymysql.allword, after - morpho/index1.html
    for x in range(3258,3336): # if text not yet in database
        text2 = trymysql(trymysql.text1.id==x).select().first()
        text1 = text2['body'].decode('utf-8')
        path = "/home/concordance/web2py/applications/test/uploads/"
        filename1=str(text2.author.id) + "_" + str(text2.n_in_group) + "_" + str(text2.id) + str('.txt')
        filename= str(path) + str(filename1)
        f = open(filename, 'w')
        f.write(text1.encode('utf-8'))
        f.close()
        text2.update_record(filename=filename)
        normal = normalize_new2(text1)
        for token in normal:
            trymysql.allword.insert(title=text2.id, word=token[0], partos=str(token[1]), author=text2.author, text_location=token[3], tense=str(token[4]), lemma=str(token[2].encode('utf-8')))
            message = "Все добавлено в базу"
    return dict(message=message)

def search_for_files():
    path = "/home/concordance/web2py/applications/test/corpus/"
    files = [f for f in listdir(path) if isfile(join(path,f)) ]
    return dict(files=files)

def verbs_all(): # show verbs in the text
    verbs1=[row['word'] for row in trymysql((trymysql.allword.author=='1')&(trymysql.allword.partos=='VERB')).select()]
    verbs1=sorted(set(verbs1))
    return dict(verbs1=verbs1)

def concordance(): # concordance of one text
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

def mystem():
    word="стояла"
    path = "/home/concordance/mystem/"
    myste=subprocess.Popen([path, '-nlc', '-e utf-8'],
                                        stdout=subprocess.PIPE,
                                        stdin=subprocess.PIPE, shell=True)
    new=myste.stdin.write(word)
    readable, _, _ = select.select([myste.stdout], [], [], 5e-3)
    stem = readable[0].readline().strip().lower()
    return dict(new=new, stem=stem)

def edit_forms():
    def record():
        rows = trymysql(trymysql.allword.title ==request.args(0)).select()
        return [row.id for row in rows]
    trymysql.allword.id.readable = True
    trymysql.allword.word.writable = True
    trymysql.allword.title.readable = True
    trymysql.allword.partos.writable = True
    trymysql.allword.tense.writable = True
    trymysql.allword.lexical_group.readable=False
    trymysql.allword.lemma.writable=True

    response.title = 'demo020'
    response.view = 'plugin_sqleditable/sample.html'
    editable = SQLEDITABLE(trymysql.allword, record=record(), deletable=True).process()
    return dict(editable=editable)

def edit_forms1():
    def record():
        titles = [x for x in range(600,700)]
        rows = trymysql((trymysql.allword.sobstv == "Geox")&(trymysql.allword.title.belongs(titles))).select()
        return [row.id for row in rows]
    trymysql.allword.id.readable = True
    trymysql.allword.word.writable = True
    trymysql.allword.title.writable = True
    trymysql.allword.partos.writable = True
    trymysql.allword.tense.writable = True
    trymysql.allword.lexical_group.readable=False
    trymysql.allword.lemma.writable=True

    response.title = 'demo020'
    response.view = 'plugin_sqleditable/sample.html'
    editable = SQLEDITABLE(trymysql.allword, record=record(), deletable=True).process()
    return dict(editable=editable)

def month():
    months = [(x, trymysql(trymysql.text1.month_writing==x).count()) for x in range(1,13)]
    return dict(months=months)

def create_xml():
    page = etree.Element('results') # create xml tree
    doc = etree.ElementTree(page)
    author_texts = [all.id for all in trymysql(trymysql.text1.author==4).select()]
    for x in author_texts:
        texts = trymysql(trymysql.text1.id==x).select()[0] # select a poem
        words_from_base = trymysql(trymysql.allword.title==x).select() # select a poem words from allword base
        title = texts.title
        author = texts.author
        f = open(texts.filename, 'rb')
        content = f.readlines()
        text = etree.SubElement(page, 'text')
        info = etree.SubElement(text, 'info')
        one = etree.SubElement(info, 'title').text = title.decode('utf-8')
        two = etree.SubElement(info, 'name').text = author.name.decode('utf-8')
        three = etree.SubElement(info, 'author').text = author.family.decode('utf-8')
        poem = etree.SubElement(text, 'poem')
        count_stanza = 1                                             # count stanzas
        line_count = 1
        word_number = words_from_base[0].id                          # get first word's id from allword base
        stanza = etree.SubElement(poem,  'stanza', number = str(count_stanza))
        for lines in content:
            if lines in ['\n', '\r\n']:
                count_stanza += 1
                stanza = etree.SubElement(poem, 'stanza', number = str(count_stanza))
            else:
                string = etree.SubElement(stanza, 'line', number=str(line_count))
                right_line = tokenize2(lines.decode('utf-8'))
                line_count +=1
                for word in right_line:
                    slovo_from_base = trymysql(trymysql.allword.id==word_number).select()[0]
                    slovo = etree.SubElement(string, 'word', pos = slovo_from_base.partos).text=word
                    word_number+=1 # update word's id
        path = "applications/test/uploads/xml/"
        new_name=path+str(texts.author.id) + ".xml"
        outFile = open(new_name, 'w')
        doc.write(outFile, pretty_print=True, xml_declaration=True, encoding='utf-16')
        outFile.close()

def create_xml1(): # save draft
    texts = trymysql(trymysql.text1.id==request.args(0)).select().first() # select a poem
    words_from_base = trymysql(trymysql.allword.title==request.args(0)).select() # select a poem words from allword base
    stop = [',', '.', ';', ':', '!', '?', '!"', '..', '!.', '...', '—', '-', '«', '»', '»', '"', '— ', '—', '!».', '!»', '4', '5', '6', '7', '8', '9', '0', " "]
    title = texts.title
    author = texts.author
    f = open(texts.filename, 'rb')
    content = f.readlines()
    page = etree.Element('results') # create xml tree
    doc = etree.ElementTree(page)
    new = etree.SubElement(page, 'text')
    info = etree.SubElement(new, 'info')
    one = etree.SubElement(info, 'title', title = title.decode('utf-8'))
    two = etree.SubElement(info, 'name', name = author.name.decode('utf-8'))
    three = etree.SubElement(info, 'author', family = author.family.decode('utf-8'))
    poem = etree.SubElement(new, 'poem', name = 'Poem')
    count_stanza = 1                                             # count stanzas
    line_count = 1
    word_number = words_from_base[0].id                          # get first word's id from allword base
    stanza = etree.SubElement(poem,  'stanza', number = str(count_stanza))
    for lines in content:
        if lines in ['\n', '\r\n']:
            count_stanza += 1
            stanza = etree.SubElement(poem, 'stanza', number = str(count_stanza))
        else:
            new_line = tokenize1(lines.decode('utf-8'))
            string = etree.SubElement(stanza, 'line', number=str(line_count), length = str(len(new_line)))
            right_line = tokenize2(lines.decode('utf-8'))
            line_count +=1
            for word in right_line:
                slovo_from_base = trymysql(trymysql.allword.id==word_number).select()[0]
                if word == new_line[-1]:
                    slovo = etree.SubElement(string, 'word', text = word, pos = slovo_from_base.partos, type='rhyme')
                else:
                    slovo = etree.SubElement(string, 'word', text = word, pos = slovo_from_base.partos)
                word_number+=1 # update word's id
    new_name=texts.filename[:-4]+".xml"
    outFile = open(new_name, 'w')
    doc.write(outFile, xml_declaration=True, encoding='utf-16')
    outFile.close()

def create_concordance():
    all_words = trymysql().select(trymysql.allword.ALL)
    part=['VERB', 'NOUN', 'ADJF', 'ADJS', 'INFN', 'GRND', 'PRTF', 'PRTS', 'ADVB']
    all1=[all.word for all in all_words if all.partos in part]
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

def test_gensim():
    all_texts = trymysql(trymysql.text1.author==4).select()
    alles = []
    for all in all_texts:
        part=['VERB', 'NOUN', 'ADJF', 'ADJS', 'INFN', 'GRND', 'PRTF', 'PRTS', 'ADVB']
        one = [all.word for all in trymysql((trymysql.allword.title==all.id)&(trymysql.allword.partos.belongs(part))).select()]
        alles.append(one)
    dictionary = corpora.Dictionary(alles)
    doc = [new.word for new in trymysql((trymysql.allword.title==24)&(trymysql.allword.partos.belongs(part))).select()]
    vec_bow = dictionary.doc2bow(doc)
    corpus = [dictionary.doc2bow(alle) for alle in alles]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=5)
    corpus_lsi = lsi[corpus_tfidf]
    vec_lsi = lsi[vec_bow]
    index = similarities.MatrixSimilarity(lsi[corpus_tfidf])
    sims = index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    topics=lsi.print_topics(5)
    return dict(sims=sims,vec_bow=vec_bow, corpus_tfidf=corpus_tfidf, topics=topics)
