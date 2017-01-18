# coding: utf8
# попробовать что-либо вида
from xml.etree import cElementTree as ET

def show1():   # show text from file
    texts = trymysql(trymysql.text1.id==request.args(0)).select().first()
    f = open(texts.filename, 'rb')
    content = f.readlines()
    image = [all.url for all in d(d.pages.text==request.args(0)).select()]
    return dict(texts=texts, content=content, image=image)

def show2(): # color the verbs
    text = trymysql(trymysql.text1.id==483).select()[0]
    words_numbers = [all.id for all in trymysql(trymysql.allword.title==text.id).select()]
    f = open(text.filename, 'rb')
    content = f.readlines()
    f.close()
    var = trymysql(trymysql.variants.title==text.id).select(orderby=trymysql.variants.line)
    words = [all.comment_text for all in var]
    lines = [all.line for all in var]
    #lines=[1,15]
    return dict(text=text, content = content, words=words, lines=lines, var=var)

def show3(): #delete words
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

def show_variants(): # try to show xml
    t = '481'
    texts = trymysql(trymysql.text1.id==t).select().first()
    filename = "/home/concordance/web2py/applications/test/uploads/xml/4/" + t + ".xml"
    x = open(filename, 'rb').read()
    root = ET.fromstring(x)
    #s = [[child.tag, child.attrib] for child in root[0][0]]
    s= []
    u = ''
    new_line =''
    variants = trymysql(trymysql.variants.title==t).select(orderby=trymysql.variants.line)
    var_numbers = [all.line for all in variants]
    var_lines = [all.comment_text for all in variants]
    book = [all.comment_book for all in variants]
    books = []
    for all in book:
        books.append(trymysql(trymysql.biblio.id==all).select()[0].short)
    books.append(texts.book)
    for st in root.iter('stanza'):
        strofa = []
        for l in st.iter('line'):
            u = l.attrib['number']
            line =[]
            for w in l.findall('word'):
                line.append(w.text)
            strofa.append([pun(line), u])
            if l.attrib['number'] in var_numbers:
                new_line = var_lines[var_numbers.index(u)]
                strofa.append(['&' + new_line, u])
        s.append(strofa)
    #for neighbor in root.iter('word'):
    #    s.append(neighbor.text)

    return dict(s=s, u=u, var_lines=var_lines, var_numbers=var_numbers, books = books)

def pun(line):
    l = ' '.join(line)
    l = l.replace(' ,', ',')
    l = l.replace(' .', ',')
    l = l.replace(' - ', '-')
    return l
