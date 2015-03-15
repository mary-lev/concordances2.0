# coding: utf8
import nltk
import pymorphy2
from tokenize1 import *
import os
from os import listdir
from os.path import isfile, join
from operator import itemgetter
import select
from lxml import etree
from plugin_sqleditable.editable import SQLEDITABLE
SQLEDITABLE.init()

def index():
    texts = trymysql().select(trymysql.author.ALL, orderby=trymysql.author.family)
    return dict(texts=texts)

def tokenize_all(): # prepares text for tokenization (decoding) and write result in database trymysql.allword, after - morpho/index1.html
    for x in range(1777,1944): # if text not yet in database
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

@auth.requires_login()
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
    author_texts = [all.id for all in trymysql(trymysql.text1.author==11).select()]
    for x in author_texts:
        texts = trymysql(trymysql.text1.id==x).select()[0] # select one poem
        words_from_base = trymysql(trymysql.allword.title==x).select().first().id # select the poem's words from allword base
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
        word_number = words_from_base                          # get first word's id from allword base
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
