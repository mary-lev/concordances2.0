# coding: utf8
from plugin_sqleditable.editable import SQLEDITABLE
SQLEDITABLE.init()
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
import csv
from categories import *

a = c('a')

def index():
    authors = trymysql().select(trymysql.author.ALL, orderby=trymysql.author.id)
    return dict(authors=authors)

#@auth.requires_login()
def slovar1():
    #file = ['/home/concordance/stem/2.txt']
    all_text = trymysql(trymysql.text1.author==66).select()
    for row in all_text:
        text = row.id
        z = 'corpus/' + str(row.author) + '/'
        z2 = 'corpus/' + str(row.author) + '/gram/'
        filename = row.filename.replace(z, z2)
        author = row.author
        with open(filename, 'rb') as fi:
            lines = fi.readlines()
        n = 0
        for line in lines:
            n += 1
            if '}-' in line:
                line=line.replace('}-', '} -')
            if '{' in line:
                line = line.split(' ')
                for word in line:
                    if '{' not in word:
                        trymysql.mystem.insert(word = word, lemma = word, title=text, author=author, partos = 'PNCT', location = n)
                    else:
                        punct=''
                        if '«' in word:
                            trymysql.mystem.insert(word = '«', lemma = '«', title=text, author=author, partos = 'PNCT', location = n)
                            word = word.replace('«', '')
                        if word.startswith('-'):
                            trymysql.mystem.insert(word = '-', lemma = '-', title=text, author=author, partos = 'PNCT', location = n)
                            word = word.replace('-', '')
                        lemma_end = word.find('{')
                        lemma = word[:lemma_end]
                        word = word[lemma_end:]
                        if not word.endswith('}'):
                            punct = word.split('}')[-1]
                            punct = punct.replace('\n', '')
                            word = ''.join(word.split('}')[:-1])
                        num = {}
                        new = word.replace('{', '').replace('}', '').split('=')
                        num['word'] = new[0]
                        l = []
                        if len(new) > 2:
                            if '|' in new[2]:
                                point = new[2].find('|')
                                ptime = new[2][1:point].split(',')
                            else:
                                ptime = new[2].split(',')
                            l += ptime
                        if len(new) > 1:
                            partos = new[1].split(',')
                            num['part'] = partos.pop(0)
                            l += partos
                        num['l'] = l
                        for p in all_parts:
                            num[p[0]] = ''.join(set(p).intersection(l))

                        try:
                            trymysql.mystem.insert(word = num['word'], lemma = lemma, title = text, partos=num['part'], anim=num['anim'], gender=num['gender'], forma = num['forma'], \
                                    comp = num['comp'], number = num['number'], cas = num['cas'], tense = num['tense'], aspect = num['aspect'], \
                                    person = num['person'], trans = num['trans'], verb = num['verb'], voice = num['voice'], \
                                    other = num['other'], author = author, location = n)
                        except:
                            trymysql.mystem.insert(word = num['word'], lemma = lemma, author = author, location = n)
                        if punct:
                            trymysql.mystem.insert(word = punct, lemma=punct, title=text, author=author, partos = 'PNCT', location = n)
    return dict(new=new, n=n)

#ypartos = ['None'] + ypartos

def count_tense_group():
    groups = [row.id for row in trymysql(trymysql.group_text.author==request.args(0)).select()]
    new=[]
    spisok = []
    if len(groups)==0:
        total = trymysql((trymysql.allword.author==request.args(0))&(trymysql.allword.tense!='None')).count()
        tense = [round(float(trymysql((trymysql.allword.author==request.args(0))&(trymysql.allword.tense==all)).count())*1.0/int(total)*100,2) for all in tenses]
        new.append(tense)
    for every in groups:
        titles = [row.id for row in trymysql(trymysql.text1.group_text==every).select()]
        total = trymysql((trymysql.allword.title.belongs(titles))&(trymysql.allword.tense!='None')).count()
        tense = [round(float(trymysql((trymysql.allword.title.belongs(titles))&(trymysql.allword.tense==all)).count())*1.0/int(total)*100,2) for all in tenses]
        name = trymysql(trymysql.group_text.id==every).select()[0]
        new.append((name['title'], tense))
    return dict(new=new)

ytense = ['None', 'praes',	'inpraes', 'praet']
ycase = ['None', 'nom', 'gen',	'dat', 'acc', 'ins', 'abl', 'part', 'loc', 'voc']
ynum = ['None', 'sg', 'pl']
yverb = ['None', 'ger', 'inf', 'partcp', 'indic', 'imper']
yform = ['None', 'brev', 'plen', 'poss']
ycomp = ['None', 'supr', 'comp']
yperson = ['None', '1p', '2p', '3p']
ygender = ['None', 'm', 'f', 'n']
yaspect = ['None', 'ipf', 'pf']
yvoice = ['None', 'act', 'pass']
yanim = ['None', 'anim', 'inan']
ytrans = ['None', 'tran', 'intr']
ynames = ['None', 'persn', 'patrn', 'famn', 'geo']

def search():
    options2 = [OPTION(texts.name, " ", texts.family, _value=texts.id) for texts in trymysql().select(trymysql.author.ALL)]
    form=FORM(TABLE(TR("Автор", SELECT(*options2, _name="author")),
                    TR("Часть речи",SELECT(*ypartos, _name="first")),
                    TR("Падеж",SELECT(*ycase, _name="second")),
                    TR("Одушевленность",SELECT(*yanim, _name="animacy")),
                    TR("Род", SELECT(*ygender, _name="gender")),
                    TR("Время", SELECT(*ytense, _name="tenses")),
                    TR("Вид", SELECT(*yaspect, _name = "aspect")),
                    TR("Залог", SELECT(*yvoice, _name = "voice")),
                    TR("Лицо", SELECT(*yperson, _name = "person")),
                    TR("Переходность", SELECT(*ytrans, _name = "trans")),
                    TR("Число", SELECT(*ynum, _name = "number")),
                    TR("Наклонение", SELECT(*yverb, _name="mood")),
                    TR("Имена собственные", SELECT(*ynames, _name="names")),
                    TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.process(formname='form_one').accepted:
        redirect(URL('search_result', args =
                     [form.vars['first'],
                      form.vars['second'],
                      form.vars['animacy'],
                      form.vars['gender'],
                      form.vars['author'],
                      form.vars['tenses'],
                      form.vars['aspect'],
                      form.vars['voice'],
                      form.vars['person'],
                      form.vars['trans'],
                      form.vars['number'],
                      form.vars['mood'],
                      form.vars['names']]))
        response.flash="form accepted"
    return dict(form=form)

def search_result():
    selected_partos = request.args(0)
    selected_form = request.args(1)
    anim = request.args(2)
    gender = request.args(3)
    author = request.args(4)
    tense = request.args(5)
    words = trymysql(trymysql.mystem.author==request.args(4)).select(trymysql.mystem.id)
    if request.args(0) != 'None':
        words = trymysql((trymysql.mystem.id.belongs(words))&(trymysql.mystem.partos==request.args(0))).select()
    if request.args(1) != 'None':
        words = trymysql((trymysql.mystem.id.belongs(words))&(trymysql.mystem.cas==request.args(1))).select()
    if request.args(2) != 'None':
        words = trymysql((trymysql.mystem.id.belongs(words))&(trymysql.mystem.anim==request.args(2))).select()
    if request.args(3) != 'None':
        words = trymysql((trymysql.mystem.id.belongs(words))&(trymysql.mystem.gender==request.args(3))).select()
    if request.args(5) != 'None':
        words = trymysql((trymysql.mystem.id.belongs(words))&(trymysql.mystem.tense==request.args(5))).select()
    if request.args(6) != 'None':
        words = trymysql((trymysql.mystem.id.belongs(words))&(trymysql.mystem.aspect==request.args(6))).select()
    if request.args(7) != 'None':
        words = trymysql((trymysql.mystem.id.belongs(words))&(trymysql.mystem.voice==request.args(7))).select()
    if request.args(8) != 'None':
        words = trymysql((trymysql.mystem.id.belongs(words))&(trymysql.mystem.person==request.args(8))).select()
    if request.args(9) != 'None':
        words = trymysql((trymysql.mystem.id.belongs(words))&(trymysql.mystem.trans==request.args(9))).select()
    if request.args(10) != 'None':
        words = trymysql((trymysql.mystem.id.belongs(words))&(trymysql.mystem.number==request.args(10))).select()
    if request.args(11) != 'None':
        words = trymysql((trymysql.mystem.id.belongs(words))&(trymysql.mystem.verb==request.args(11))).select()
    if request.args(12) != 'None':
        words = trymysql((trymysql.mystem.id.belongs(words))&(trymysql.mystem.other==request.args(12))).select()
    message=""
    strings=[]
    if len(words) == 0:
        message = "Sorry, nothing found"
    else:
        for all in words:
            location = all.location
            title1 = trymysql(trymysql.text1.id==int(all.title)).select()[0]
            title=title1.title
            author= (title1.author.name, title1.author.family)
            string="..."
            blue_word = all.lemma
            for x in range(all.id-6, all.id+6):
                try:
                    for_string = trymysql(trymysql.mystem.id==x).select()[0]
                    string= string + " " + str(for_string.lemma)
                except:
                    pass
            strings.append((string +"...", title, author, int(title1.id), all.id, blue_word))
    response.title = 'Результаты поиска'
    return dict(strings=strings, message=message)

def fix():
    rows = d((d.mystem.word.like('%?'))&(d.mystem.word!='?')).select(groupby=d.mystem.word)
    words = [all.word for all in rows]
    with open('/home/concordance/web2py/applications/test/corpus/fixlist.txt', 'wb') as f:
        f.write('\n'.join(words))
    return dict(a = len(words))

@auth.requires_login()
def correct_word():
    record = trymysql.mystem(request.args(0))
    form = SQLFORM(trymysql.mystem, record)
    if form.process().accepted:
       response.flash = 'form accepted'
    return dict(form=form)

def correct():
    record = trymysql(trymysql.mystem.id==request.args(0)).select()[0]
    text= trymysql(trymysql.text1.id == record.title).select()[0]
    f = open(text.filename, 'rb')
    author = text.author.family
    a_name = text.author.name
    title = text.title
    content = f.readlines()
    form=FORM(TABLE(TR("Слово", INPUT(_type='text', _name="word", value=record.word)),
                    TR("Форма", INPUT(_type='text', _name = "lemma", value = record.lemma)),
                    TR("Часть речи",SELECT(*ypartos, _name="first", value = record.partos)),
                    TR("Падеж",SELECT(*ycase, _name="second", value=record.cas)),
                    TR("Одушевленность",SELECT(*yanim, _name="animacy", value = record.anim)),
                    TR("Род", SELECT(*ygender, _name="gender", value = record.gender)),
                    TR("Время", SELECT(*ytense, _name="tenses", value = record.tense)),
                    TR("Вид", SELECT(*yaspect, _name = "aspect", value= record.aspect)),
                    TR("Залог", SELECT(*yvoice, _name = "voice", value = record.voice)),
                    TR("Лицо", SELECT(*yperson, _name = "person", value = record.person)),
                    TR("Переходность", SELECT(*ytrans, _name = "trans", value = record.trans)),
                    TR("Число", SELECT(*ynum, _name = "number", value = record.number)),
                    TR("Наклонение", SELECT(*yverb, _name="mood", value = record.verb)),
                    TR("Имена собственные", SELECT(*ynames, _name="names", value = record.other)),
                    TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.process().accepted:
        record.update_record(word = form.vars['word'],
                      partos = form.vars['first'],
                      cas = form.vars['second'],
                      anim = form.vars['animacy'],
                      gendr = form.vars['gender'],
                      tense = form.vars['tense'],
                      aspect = form.vars['aspect'],
                      voice = form.vars['voice'],
                      person = form.vars['person'],
                      transitivity = form.vars['trans'],
                      number = form.vars['number'],
                      verb = form.vars['mood'],
                      other = form.vars['names'])
        response.flash="form accepted"
    return dict(form=form, content = content, author=author, a_name = a_name, title = title, word=record.lemma)

def index1(): # parse by pymorphy for trymysql.allword
    titles = [x for x in range(7848,7941)] # last: 3500, 7088, 10261
    texts = trymysql(trymysql.allword.title.belongs(titles)).select()
    for all in texts:
        the_word = all.lemma.decode("utf-8")
        normal = morph.parse(the_word)[0]
        parsed_other = parse_tags(normal.tag, other)['result']
        parsed_style = parse_tags(normal.tag, style)['result']
        parsed_name = parse_tags(normal.tag, names[1:])['result']
        if all.partos != 'None':
            all.update_record(anim = str(normal.tag.animacy), gendr=str(normal.tag.gender), number = str(normal.tag.number), cas = str(normal.tag.case), tense = str(normal.tag.tense), aspect = str(normal.tag.aspect), person = str(normal.tag.person), transitivity= str(normal.tag.transitivity), mood = str(normal.tag.mood), involvment = str(normal.tag.involvement), voice = str(normal.tag.voice), sobstv=parsed_name, style = parsed_style, other = parsed_other)
    return dict()

def parse_tags(tags, list_tags):
    parsed = [x for x in list_tags if x in tags]
    result = 'None'
    for all in parsed:
        if all != 'None':
            result = str(all)
    return dict(result=result)
