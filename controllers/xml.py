# coding: utf8
# попробовать что-либо вида
from lxml import etree
from tokenize1 import *

def index(): return dict(message="hello from xml.py")

def create_xml():
    n = 1
    author_texts = [all.id for all in trymysql(trymysql.text1.author==n).select()]
    author_id = trymysql(trymysql.author.id==n).select().first()
    page = etree.Element('all') # create xml tree
    doc = etree.ElementTree(page)
    author = etree.SubElement(page, 'author')
    family = etree.SubElement(author, 'family').text=author_id.family.decode('utf-8')
    name = etree.SubElement(author, 'family').text=author_id.name.decode('utf-8')
    for x in author_texts[1:]:
        texts = trymysql(trymysql.text1.id==int(x)).select()[0] # select one poem
        words_from_base = trymysql(trymysql.allword.title==int(x)).select() # select the poem's words from allword base
        f = open(texts.filename, 'rb')
        content = f.readlines()
        f.close()
        text = etree.SubElement(page, 'text')
        info = etree.SubElement(text, 'info')
        one = etree.SubElement(info, 'title').text = texts.title.decode('utf-8')
        if isinstance(texts.under_title, str):
            subtitle = etree.SubElement(info, 'subtitle').text=texts.under_title.decode('utf-8')
        if isinstance(texts.group_text.title, str):
            group = etree.SubElement(info, 'group').text=texts.group_text.title.decode('utf-8')
        if len(texts.dedication)>0:
            dedication = etree.SubElement(info, 'dedication').text = texts.dedication.decode('utf-8')
        try:
            year = etree.SubElement(info, 'year').text = texts.year_writing
            month = etree.SubElement(info, 'month').text = texts.month_writing
            day = etree.SubElement(info, 'day').text = texts.day_writing
        except:
            pass
        poem = etree.SubElement(text, 'poem')
        count_stanza = 1                                             # count stanzas
        line_count = 1                   # get first word's id from allword base
        word_count = 0
        word_number = words_from_base[0].id
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
                    if len(words_from_base)>0:
                        if words_from_base[word_count].id != word_number:
                            slovo=etree.SubElement(string, 'werd')
                            word_number+=1
                        else:
                            slovo = etree.SubElement(string, 'word', number=str(words_from_base[word_count].id), pos = words_from_base[word_count].partos).text=words_from_base[word_count].lemma.decode('utf-8')
                            word_count +=1
                            word_number +=1
                    else:
                        slovo=etree.SubElement(string, 'wurd')
                        word_number +=1
                        word_count += 1
    path = "applications/test/uploads/xml/"
    new_name=path + str(n) + ".xml"
    outFile = open(new_name, 'w')
    doc.write(outFile, pretty_print=True, xml_declaration=True, encoding='utf-16')
    outFile.close()

def create_xml_unique(): # create one xml for one text
    author_texts = [all.id for all in trymysql(trymysql.text1.author==13).select()] # 9458, 10188, 10261 for author 8, 8236 for author 9
    for x in author_texts:
        page = etree.Element('results') # create xml tree
        doc = etree.ElementTree(page)
        texts = trymysql(trymysql.text1.id==int(x)).select().first() # select one poem
        words_from_base = trymysql(trymysql.allword.title==int(x)).select().first().id # select the poem's words from allword base
        title = texts.title
        author = texts.author
        f = open(texts.filename, 'rb')
        content = f.readlines()
        f.close()
        text = etree.SubElement(page, 'text')
        info = etree.SubElement(text, 'info')
        one = etree.SubElement(info, 'title').text = title.decode('utf-8')
        two = etree.SubElement(info, 'name').text = author.name.decode('utf-8')
        three = etree.SubElement(info, 'author').text = author.family.decode('utf-8')
        poem = etree.SubElement(text, 'poem')
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
        DECLARATION = """<?xml version="1.0" encoding="utf-8"?>
        <?xml-stylesheet type="text/xsl" href="style.xslt"?>\n"""
        with open(new_name, 'w') as output: # would be better to write to temp file and rename
            output.write(DECLARATION)
            doc.write(output, xml_declaration=False, pretty_print=True, encoding='utf-8')
            output.close()

def table_as_xml(): #no view yet, for view: {{=TAG(r)}}
    words = trymysql(trymysql.allword.title==15).select()
    r = words.xml()
    return dict(r=r)
