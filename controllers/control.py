# coding: utf8
import simplejson
import pymorphy2
from tokenize1 import *
import os
from os import listdir
from os.path import isfile, join
from lxml import etree
from plugin_sqleditable.editable import SQLEDITABLE
SQLEDITABLE.init()

def index():
    texts = trymysql().select(trymysql.author.ALL, orderby=trymysql.author.family)
    return dict(texts=texts)

def corpus():
    texts = [[all.filename, int(all.id)] for all in trymysql(trymysql.text1.author==21).select()]
    for all in texts:
        f = open(all[0], 'rb')
        new = f.readlines()
        f.close()
        path = '/home/concordance/web2py/applications/test/corpus/21/' + str(all[1]) + '.txt'
        newf = open(path, 'wb')
        newf.writelines(new)
        newf.close()
        os.remove(all[0])
        record = trymysql(trymysql.text1.id == str(all[1])).select().first()
        record.update_record(filename=path)
    return dict(new=new, texts=texts, path=path)

def tokenize_all(): # prepares text for tokenization (decoding) and write result in database trymysql.allword, after - morpho/index1.html
    for x in range(10260,10275): # if text not yet in database (last:4811,7088, 10260)
        text2 = trymysql(trymysql.text1.id==x).select().first()
        text1 = text2['body'].decode('utf-8')
        path = "/home/concordance/web2py/applications/test/uploads/sologub/"
        filename1=str(text2.author.id) + "_" + str(text2.n_in_group) + "_" + str(text2.id) + str('.txt')
        filename= str(path) + str(filename1)
        f = open(filename, 'w')
        f.write(text1.encode('utf-8'))
        f.close()
        text2.update_record(filename=filename)
        normal = normalize_new2(text1, 0)
        for token in normal:
            trymysql.allword.insert(title=text2.id, word=token[0], partos=str(token[1]), author=text2.author, text_location=token[3], tense=str(token[4]), lemma=str(token[2].encode('utf-8')))
            message = "Все добавлено в базу"
    return dict(message=message)

names = ['None', 'Abbr', 'Name', 'Surn', 'Patr', 'Geox', 'Init']
style = ['Infr', 'Slng', 'Arch', 'Litr', 'Erro', 'Dist']
other = ['Ques', 'Dmns', 'Prnt', 'Prdx', 'Af-p', 'Anph', 'Inmx', 'V-be', 'V-en', 'V-ie', 'V-bi', 'V-ey', 'V-oy', 'Cmp2', 'V-ej', 'Fimp', 'Coun', 'Coll', 'V-sh', 'Vpre', 'Supr', 'Qual', 'Apro', 'Anum', 'Poss']

def check_old():
    n = []
    filename2="/home/concordance/web2py/applications/test/uploads/newdict/verbs.txt"
    with open(filename2,'rb') as inf:
        ispr = inf.read()
        inf.close()
    for new in ispr.split():
        words = trymysql(trymysql.allword.lemma==new).select()
        for all in words:
            n.append(all.word)
            all.update_record(partos='VERB', word=new, gendr='None', number='None', cas='None', tense='None', aspect='None', person='None', transitivity= 'None', mood = 'None', involvment = 'None', voice = 'None', sobstv='None', style = 'Infr')
    return dict(ispr=ispr, n=n)

def check_old1():
    morph = pymorphy2.MorphAnalyzer()
    mist = []
    filename2="/home/concordance/web2py/applications/test/uploads/newdict/ispr3.txt"
    with open(filename2,'rb') as inf:
        ispr = eval(inf.read())
    for new in ispr.keys():
        words = trymysql(trymysql.allword.lemma==new).select()
        normal = morph.parse(new.decode('utf-8'))[ispr[new]]
        parsed_other = parse_tags(normal.tag, other)['result']
        parsed_style = parse_tags(normal.tag, style)['result']
        parsed_name = parse_tags(normal.tag, names[1:])['result']
        for all in words:
            all.update_record(word=normal.normal_form, partos = str(normal.tag.POS), anim = str(normal.tag.animacy), gendr=str(normal.tag.gender), number = str(normal.tag.number), cas = str(normal.tag.case), tense = str(normal.tag.tense), aspect = str(normal.tag.aspect), person = str(normal.tag.person), transitivity= str(normal.tag.transitivity), mood = str(normal.tag.mood), involvment = str(normal.tag.involvement), voice = str(normal.tag.voice), sobstv=parsed_name, style = parsed_style, other = parsed_other)
    return dict(ispr=ispr, mist = mist)

def parse_tags(tags, list_tags):
    parsed = [x for x in list_tags if x in tags]
    result = 'None'
    for all in parsed:
        if all != 'None':
            result = str(all)
    return dict(result=result)

@auth.requires_login()
def search_for_files():
    path = "/home/concordance/web2py/applications/test/corpus/"
    files = [f for f in listdir(path) if isfile(join(path,f)) ]
    filename=str(path)+files[0]
    new = open(filename, 'rb')
    content = new.readlines()
    poems = []
    text = {}
    n=0
    stih=[]
    zagl=ded=year=day=month=location=epi=a_epi=''
    string_number=0
    for all in content:
        string_number +=1
        if 'NNN' in all:
            zagl = all[3:]
        elif 'ggg' in all:
            year = all[3:]
        elif 'mmm' in all:
            month = all[3:]
        elif 'dday' in all:
            day = all[4:]
        elif 'lll' in all:
            location = all[3:]
        elif 'DDD' in all:
            ded = all[3:]
        elif 'EPI' in all:
            epi = all[3:]
        elif 'AUT' in all:
            a_epi = all[3:]
        elif "*" in all:
            text['t']=stih
            poems.append(text)
            trymysql.text1.insert(title=zagl, first_string=stih[0]+str("..."), year_writing=year, epigraph = epi, epigraph_author = a_epi, dedication= ded, month_writing=month, day_writing=day, author=8, group_text=81, writing_location=location, body = ''.join(text['t']))
            stih = []
            text= {}
            year=''
            zagl=''
            month=''
            day=''
            location=''
            ded=epi=a_epi=''
            n+=1
            string_number=0
        else:
            stih.append(all)
    return dict(poems=poems)

def select_one(content):
    new = content.count('*')
    poems = []
    content = ' '.join(content)
    for all in range(new):
        end = content.index('*')
        poems.append(content[:end])
        content = content[end-1:]
    return dict(poems=poems)

def verbs_all(): # show verbs in the text
    verbs1=[row['word'] for row in trymysql((trymysql.allword.author=='1')&(trymysql.allword.partos=='VERB')).select()]
    verbs1=sorted(set(verbs1))
    return dict(verbs1=verbs1)

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

@auth.requires_login()
def edit_forms1():
    def record():
        titles = [x for x in range(800,900)]
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
    ## author_texts = [all.id for all in trymysql(trymysql.text1.author==11).select()]
    for x in range(483,484):
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
        #outFile = open(new_name, 'w')
        #doc.write(outFile, pretty_print=True, xml_declaration=True, encoding='utf-16')
        #outFile.close()
        DECLARATION = """<?xml version="1.0" encoding="utf-8"?>
        <?xml-stylesheet type="text/xsl" href="style.xslt"?>\n"""
        with open(new_name, 'w') as output: # would be better to write to temp file and rename
            output.write(DECLARATION)
            doc.write(output, xml_declaration=False, pretty_print=True, encoding='utf-8')

def table_as_xml(): #no view yet, for view: {{=TAG(r)}}
    words = trymysql(trymysql.allword.title==15).select()
    r = words.xml()
    return dict(r=r)

def create_concordance():
    update_word= []
    for x in range(9700, 10000):
        texts = trymysql(trymysql.allword.title==x).select()
        words = [all.word for all in texts]
        for w in words:
            if trymysql(trymysql.concordances.word==w).isempty()==True:
                trymysql.concordances.insert(word=w)
                update_word.append(w) # words inserted in concordances table
    return dict(update_word=update_word)
#    part=['VERB', 'NOUN', 'ADJF', 'ADJS', 'INFN', 'GRND', 'PRTF', 'PRTS', 'ADVB']
#    all1=[all.word for all in trymysql(trymysql.allword.author==1).select()]
#    slovar = [all.word for all in trymysql(trymysql.concordance.id>0).select()]
#    words=sorted(set(all1))
#    for x in words:
#        if x not in slovar:
#            trymysql.concordance.insert(word=x)
#    return dict(part=words[:100])

def see_concordances():
    n=[]
    s = 1
    words = trymysql(trymysql.concordances.word.like('а%')).select()
    w = [all.word for all in words]
    w = sorted(w)
    for all in w:
        name = 'nomer'+str(s)
        name = FORM(INPUT(_name='myform', value=all, requires=IS_NOT_EMPTY()),
                    INPUT(_type='submit'), action='', method="GET")
        if name.accepts(request, session, keepvalues=True, formname=all):
 #           response.flash = 'yes!'
            trymysql.color.insert(word=all)
            s+=1
        n.append(name)
    return dict(n=n)

def create_number(): #intrymysql.allword.concordance_number connected to trymysql.concordances.id
    for all in trymysql((trymysql.concordances.id>3499)&(trymysql.concordances.id<3550)).select():
        words = trymysql((trymysql.allword.word==all.word)&(trymysql.allword.partos!='PNCT')).select()
        for w in words:
            w.update_record(concordance_number=all.id)
    #for all in trymysql((trymysql.allword.id>49999)&(trymysql.allword.id<60000)).select():
    #    number = trymysql(trymysql.concordances.word==all.word).select().first().id
     #   all.update_record(concordance_number= number)
    return dict(message="OK")

def save_files():
    t = []
    texts = [all.filename for all in trymysql(trymysql.text1.author==request.args(0)).select()]
    for all in texts:
        f = open(all, 'rb')
        content = f.readlines()
        t.append(content)
    f = '/home/concordance/deposit/poems.txt'
    with open(f, 'w') as ff:
        for all in t:
            print>>ff, all
