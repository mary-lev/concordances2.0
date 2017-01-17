# coding: utf8
import nltk
import pymorphy2
from tokenize1 import *
import os
from os import listdir
from os.path import isfile, join
from operator import itemgetter
from json2html import *
from gluon.serializers import json
import collections

# json structure
# poem:
# info: author (name, family), text (title, group_text, date: day, month, year, location, publication, epigraph: text & author of epigraph,)
# text: stanza: count line, line: count words, word: pos, number in allword, variant, comments.

def index():
    text = trymysql(trymysql.text1.id==request.args(0)).select().first()
    words_from_base=[all.id for all in trymysql(trymysql.allword.title==request.args(0)).select()]
    f = open(text.filename, 'rb')
    content = f.readlines()
    f.close()
    count_stanza = 1
    line_count = 1
    word_number = words_from_base[0]                       # get first word's id from allword base
    lines_all={}
    stanza={}
    for lines in content:
        if lines in ['\n', '\r\n']:
            stanza[count_stanza] = lines_all
            lines_all = {}
            count_stanza += 1
        else:
            right_line = tokenize2(lines.decode('utf-8'))
            all_words_in_line={}
            for word in right_line:
                if word_number in words_from_base:
                    if word_number in [all.word_first for all in trymysql(trymysql.variants.title==request.args(0)).select()]:
                        all_words_in_line[word_number]= {'word_number': word_number, 'form': word, 'partos': trymysql(trymysql.allword.id==word_number).select().first().partos, 'variant': trymysql(trymysql.variants.word_first==word_number).select().first().comment_text}
                    else:
                        all_words_in_line[word_number]={'word_number': word_number, 'form': word, 'partos': trymysql(trymysql.allword.id==word_number).select().first().partos}
                    word_number+=1 # update word's id
            lines_all[line_count] = collections.OrderedDict(sorted(all_words_in_line.items()))
            line_count +=1
            all_words_in_line={}
    stanza[count_stanza] = lines_all
    info = [{'author': [text.author.name, text.author.family]}, {'text_info': [text.title], 'date': [text.day_writing, text.month_writing, text.year_writing]}]
    all = {'info': info, 'text': stanza}
    c = json2html.convert(json = all, table_attributes="class=\"table table-bordered table-hover\"")
    return dict(c=c)

def create_json(): # create one json for one text
    for x in range(483,484):
        texts = trymysql(trymysql.text1.id==int(x)).select().first() # select one poem in text1 base
        words_from_base = trymysql(trymysql.allword.title==int(x)).select().first().id # select the poem's words from allword base
        title = texts.title
        author = texts.author
        f = open(texts.filename, 'rb')
        content = f.readlines()
        f.close()
        count_stanza = 1                                             # count stanzas
        line_count = 1
        word_number = words_from_base                       # get first word's id from allword base
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
                    if trymysql(trymysql.allword.id==word_number).select().first() is None:
                        slovo = etree.SubElement(string, 'werd', number = str(word_number))
                    else:
                        if trymysql(trymysql.allword.id==word_number).select().first().id in [all.id for all in trymysql(trymysql.allword.title==x).select()]:
                            slovo_from_base = trymysql(trymysql.allword.id==word_number).select().first()
                            if slovo_from_base.id in [all.word_first for all in trymysql(trymysql.variants.id>0).select()]: #write variant of word if any
                                slovo = etree.SubElement(string, 'word', number=str(slovo_from_base.id), variant = trymysql(trymysql.variants.word_first==slovo_from_base.id).select().first()['comment_text'].decode('utf-8'), pos = slovo_from_base.partos).text=slovo_from_base.lemma.decode('utf-8')
                            else:
                                slovo = etree.SubElement(string, 'word', number=str(slovo_from_base.id), pos = slovo_from_base.partos).text=slovo_from_base.lemma.decode('utf-8')
                    word_number+=1 # update word's id
        path = "applications/test/uploads/xml/13/"
        new_name=path+str(x) + ".xml"
        #outFile = open(new_name, 'w')
        #doc.write(outFile, pretty_print=True, xml_declaration=True, encoding='utf-16')
        #outFile.close()
        DECLARATION = """<?xml version="1.0" encoding="utf-8"?>
        <?xml-stylesheet type="text/xsl" href="style.xslt"?>\n"""
        with open(new_name, 'w') as output: # would be better to write to temp file and rename
            output.write(DECLARATION)
            doc.write(output, xml_declaration=False, pretty_print=True, encoding='utf-8')
