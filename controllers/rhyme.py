# coding: utf8
import nltk
import pymorphy2
from operator import itemgetter
import string
import os
from os import listdir
from os.path import isfile, join
import lxml.etree

def index():
    return dict()

def index1():
    tt = trymysql(trymysql.text1.author==14).select()
    ids = [all.id for all in tt]
    for x in ids:
        words=[]
        text = trymysql(trymysql.text1.id==x).select().first()
        f = open(text.filename, 'rb')
        content = f.readlines()
        f.close()
        for all in content:
            new = nltk.wordpunct_tokenize(all.decode('utf-8'))
            new = [x for x in new if x.isalpha() or x.isspace()] # delete punctuation and numbers
            if len(new)>0:
                words.append(new[-1].lower())
        r = (' '.join(words)).encode('utf-8')
        trymysql.stih.insert(title=text.id, author=text.author, rhymes = r) # insert into database, not in file
    return dict(words=words)

def search():
    f = open('/home/concordance/web2py/applications/test/rhymes/t_balmont.txt', 'r')
    content = f.readlines()
    f.close()
    rhyme = []
    a = 0
    for all in content:
        poem = all.split()
        if len(poem)>3:
            if test_ABAB(poem) is True:
                rhyme.append(rhymes(poem, 'ABAB'))
            elif test_AABB(poem) is True:
                rhyme.append(rhymes(poem, 'AABB'))
            elif test_ABBA(poem) is True:
                rhyme.append(rhymes(poem, 'ABBA'))
            elif test_ABAC(poem) is True:
                rhyme.append(rhymes(poem, 'ABAC'))
            elif test_ABCB(poem) is True:
                rhyme.append(rhymes(poem, 'ABCB'))
            else:
                rhyme.append('Don\'t know')
                a += 1
        else:
            rhyme.append(len(poem))
    return dict(rhyme=rhyme, a=a)

dubl = ['с', 'п', 'т', 'к', 'ш', 'ф', 'а', 'и']
dubl2 = ['з', 'б', 'д', 'г', 'ж', 'в', 'о', 'е']

def test_dubl(a, b): # проверяем звонкие и глухие согласные
    if a in dubl and b in dubl2:
        if dubl.index(a) == dubl2.index(b):
            return True
    if a in dubl2 and b in dubl:
        if dubl2.index(a) == dubl.index(b):
            return True

def test_ABCB(poem):
    t = []
    for all in poem[1::2]:
        try:
            if all[-1] == poem[poem.index(all)+2][-1]:
                t.append('1')
            elif test_dubl(all[-1], poem[poem.index(all)+2][-1]) is True:
                t.append('1')
            else:
                t.append('0')
        except:
            pass
    return c_t(t)

def test_ABAC(poem):
    t = []
    for all in poem[::2]:
        try:
            if all[-1] == poem[poem.index(all)+2][-1]:
                t.append('1')
            else:
                t.append('0')
        except:
            pass
    return c_t(t)

def test_AABB(poem):
    t = []
    for all in poem[::2]:
        try:
            if all[-3:] == poem[poem.index(all)+1][-3:]:
                t.append('1')
            else:
                t.append('0')
        except:
            pass
    return c_t(t)

def test_ABAB(poem):
    t = []
    for all in poem[::2]:
        try:
            if all[-1] == poem[poem.index(all)+2][-1]:
                t.append('1')
            else:
                t.append('0')
        except:
            pass
    for all in poem[1::2]:
        try:
            if all[-1] == poem[poem.index(all)+2][-1]:
                t.append('1')
            else:
                t.append('0')
        except:
            pass
    return c_t(t)

def test_ABBA(poem):
    t = []
    for all in poem[::4]:
        try:
            if all[-1] == poem[poem.index(all)+3][-1]:
                t.append('1')
            else:
                t.append('0')
        except:
            pass
    for all in poem[1::4]:
        try:
            if all[-1] == poem[poem.index(all)+1][-1]:
                t.append('1')
            else:
                t.append('0')
        except:
            pass
    return c_t(t)


def rhymes(line, type_r):
    rhymes = []
    if type_r == 'ABBA':
        for all in line:
            if all != 'None':
                if line.index(all)%2 == 0:
                    try:
                        rhymes.append([all, line[line.index(all)+3]])
                        line[line.index(all)+3] = 'None'
                    except:
                        rhymes.append('end')
                else:
                    try:
                        rhymes.append([all, line[line.index(all)+1]])
                        line[line.index(all)+1] = 'None'
                    except:
                        rhymes.append('end')
    if type_r == 'AABB':
        p1 = line[::2]
        p2 = line[1::2]
        if len(p1)==len(p2):
            for x in p1:
                rhymes.append([x, p2[p1.index(x)]])
        else:
            rhymes = 'uneven'
    if type_r == 'ABAB':
        for all in line:
            try:
                if all != 'None':
                    rhymes.append([all, line[line.index(all)+2]])
                    line[line.index(all)+2] = 'None'
            except:
                pass
    if type_r == 'ABAC':
        for all in line[::2]:
            if all != 'None':
                try:
                    rhymes.append([all, line[line.index(all)+2]])
                    line[line.index(all)+2] = 'None'
                except:
                    pass
    if type_r == 'ABCB':
        for all in line[1::2]:
            if all != 'None':
                try:
                    rhymes.append([all, line[line.index(all)+2]])
                    line[line.index(all)+2] = 'None'
                except:
                    pass
    return rhymes

def c_t(t):
    if t.count('1') >= t.count('0'):
        return True
    else:
        return False

def count_stanza():
    texts = trymysql(trymysql.text1.author==21).select()
    path = '/home/concordance/web2py/applications/test/uploads/xml/'
    for all in texts[:-1]:
        filename = path + str(all.author) + '/' + str(all.id) + '.xml'
        doc = lxml.etree.parse(filename)
        count = doc.xpath('count(//line)')
        cars = doc.xpath('//stanza')
        n = []
        for car in cars:
            colors = car.xpath('count(.//line)')
            if int(colors)>0:
                n.append(int(colors))
 #       for new in st:
 #           if all(new == item for item in n) is True:
 #               s = new
        s = check_s(n)
        t = trymysql(trymysql.stih.title == all.id).select()[0]
        t.update_record(kol_strok=int(count), strofa = n, type_s = s)
    return dict()

st = [2, 3, 4, 5, 6, 7, 8]
st_2 = ['Двустишие', 'Трехстишие', 'Четверостишие', 'Пятистишие', 'Шестистишие', 'Семистишие', 'Восьмистишие']
opt = []

for all in st:
    opt.append([all, st_2[st.index(all)]])

def check_s(n):
    s=''
    for new in st:
        if all(new == item for item in n) is True:
            s = new
    return s

def form_search():
    options = [OPTION(o[1], _value=o[0]) for o in opt]
    options2 = [OPTION(texts.name, " ", texts.family, _value=texts.id) for texts in trymysql().select(trymysql.author.ALL)]
    form=FORM(TABLE(TR("Тип строфы",SELECT(*options, _name="first")),
                    TR("Автор",SELECT(*options2, _name="second")),
                    TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.process(formname='form_one').accepted:
        redirect(URL('find_s', args = [form.vars['first'], form.vars['second']]))
        response.flash="form accepted"
    return dict(form=form)

def find_s():
    texts = [all.title for all in trymysql((trymysql.stih.type_s==int(request.args(0)))&(trymysql.stih.author==request.args(1))).select()]
    ttt = trymysql(trymysql.text1.id.belongs(texts)).select()
    return dict(ttt=ttt)

def find_sonet():
    sonnet = ['|4|4|3|3|', '|4|4|4|2|', '|4|4|6|', '|4|4|2|2|2|', '|12|2|']
    texts = [t.title for t in trymysql(trymysql.stih.strofa.belongs(sonnet)).select()]
    ttt = trymysql(trymysql.text1.id.belongs(texts)).select(orderby=trymysql.text1.author)
    return dict(ttt=ttt)

def find_2():
    texts = trymysql(trymysql.stih.type_s=='4').select()
    r = []
#    ri = [all.rhymes for all in texts]
    for all in texts:
        ttt = all.rhymes.split()
        test = all.trhymes.split(' ')
        p1 = ttt[::2]
        p2 = ttt[1::2]
        if test_AABB(test) is True:
            for p in p1:
                #                if t1[p1.index(p)][-1] == t2[p1.index(p)][-1]:
                r.append([p.decode('utf-8'), p2[p1.index(p)].decode('utf-8'), all.title])
        elif test_ABAB(test) is True:
            if len(test) > 2:
                new = rhymes(ttt, 'ABAB')
                for n in new:
                    r.append([n[0], n[1], all.title])
        elif test_ABBA(test) is True:
            if len(test) > 2:
                new = rhymes(ttt, 'ABBA')
                for n in new:
                    r.append([n[0], n[1], all.title])
        else:
            r.append([test[0], test[1], all.title])

    return dict(r=r)
