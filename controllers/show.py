# coding: utf8
# попробовать что-либо вида
from xml.etree import cElementTree as ET
import difflib
import re

def show1():   # show text from file
    texts = trymysql(trymysql.text1.id==request.args(0)).select().first()
    f = open(texts.filename, 'rb')
    content = f.readlines()
    image = [all.url for all in d(d.pages.text==request.args(0)).select()]
    return dict(texts=texts, content=content, image=image)

def show2(): # варианты из текстового файла, проблема с пустыми строками между строфами
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

def show3(): #variants from txt files
    text = trymysql(trymysql.text1.id==request.args(0)).select().first()
    filename1 = text.filename
    book = [text.book]
    t1 = open(filename1, 'rb')
    text1 = t1.readlines()
    # ищем варианты в trymysql.drafts
    variant = trymysql(trymysql.drafts.text==request.args(0)).select()
    table = []
    biblio = [text.book]
    biblio1=[]
    other = []
    seq = []
    for all in variant:
        filename2 = all.filename
        book.append(all.book.short)
        t2 = open(filename2, 'rb')
        text2 = t2.readlines()
        # сравниваем тексты
        d = difflib.Differ()
        result = list(d.compare(text1, text2))
        table.append(result)
        biblio1.append(trymysql(trymysql.biblio.id==all.book).select()[0])
#str(all.book.id) + '. '+ all.book.title + '. ' + all.book.city + ': ' + all.book.editor + ', ' + all.book.year + '. ' + all.book.part + ". C. " + all.book_page + '.')
        n = {}
        n['title'] = all.title.upper()
        n['dedication'] = all.dedication
        n['epi'] = all.epi
        n['epi_author'] = all.epi_author
        n['epi_book'] = all.epi_book
        other.append(n)
    #for res in table:
    count = 0
    s = []
    n = 0
    clear = [line for line in table[n] if not line.startswith('?') and '|' not in line]
    while len(clear)>0:
        if clear[count].startswith('-'):
            try:
                next_line = clear[count+1][2:]
                cline = clear[count][2:]
                p = ['(', ')', '[', ']', "’"]
                for all in p:
                    next_line = next_line.replace(all, '')
                    cline = cline.replace(all, '')
                next_line = re.findall(ur"\w+[ ]|\w+|[,]|[.]", next_line.decode('utf-8'), re.U)
                next_line = [all.replace(' ', '') for all in next_line]
                cline = re.findall(ur"\w+[ ]|\w+|[,]|[.]", cline.decode('utf-8'), re.U)
                cline = [all.replace(' ', '') for all in cline]
                d = difflib.Differ(charjunk=difflib.IS_CHARACTER_JUNK )
                s1 = list(d.compare(cline, next_line))
                s.append(s1)
                clear.remove(clear[count+1])
                c= next_line
            except:
                pass
        else:
            s.append(clear[count][2:].split())
            #c = re.findall(ur"\w+[ ]|\w+|[,]|[.]", clear[count].decode('utf-8'), re.U)
        clear.remove(clear[count])
    return dict(book=book, table=table, text=text, biblio=biblio, biblio1=biblio1, other=other, s=s, n=n)

def zatochnik():
    #text = trymysql(trymysql.text1.id==10277).select().first()
    variant = trymysql(trymysql.drafts.text==10277).select()
    text = variant[int(request.args(0))]
    variant.exclude((lambda r: r.id == text.id))
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
            p = ['(', ')', '[', ']', "’"]
            for all in p:
                t = t.replace(all, '')
                l = l.replace(all, '')
            l = re.findall(ur"\w+[ ]|\w+|[,]|[.]", l.decode('utf-8'), re.U)
            l = [all.replace(' ', '') for all in l]
            t = re.findall(ur"\w+[ ]|\w+|[,]|[.]", t.decode('utf-8'), re.U)
            t = [all.replace(' ', '') for all in t]
            d = difflib.Differ()
            r = list(d.compare(l, t))
            result.append(r)
            t=''
        table.append(result)
    return dict(table=table, text=text)

def show_variants(): # try to show xml
    t = '483'
    texts = trymysql(trymysql.text1.id==t).select().first()
    filename = "/home/concordance/web2py/applications/test/uploads/xml/4/" + t + ".xml"
    x = open(filename, 'rb').read()
    root = ET.fromstring(x) # парсим xml
    s= [] # это будет текст
    u = '' # это будет номер строки
    new_line ='' # это будет вариантная строка
    variants = trymysql(trymysql.variants.title==t).select(orderby=trymysql.variants.line) # выбираем записи про варианты строк для этого текста из базы
    var_numbers = [all.line for all in variants] # выбираем номера строк, где есть варианты
    var_lines = [all.comment_text for all in variants] # выбираем вариантные строки из базы
    book = [all.comment_book for all in variants] # выбираем источники вариантов
    books = [texts.book] # источник основной редакции из trymysql.text1
    for all in book:
        books.append(trymysql(trymysql.biblio.id==all).select()[0].short) # сокращенное название изданий, содержащих варианты строк
    for st in root.iter('stanza'): # парсим xml
        strofa = [] # это будет строфа
        for l in st.iter('line'):
            u = l.attrib['number'] # проверяем номер выпарсенной строки
            line =[] # это будет строчка
            for w in l.findall('word'):
                line.append(w.text)
            strofa.append([pun(line), u]) # чистим пробелы в строке
            if l.attrib['number'] in var_numbers: # проверяем, есть ли у строки варианты по ее порядковому номеру в тексте
                new_line = var_lines[var_numbers.index(u)] # выбираем вариантную строку из списка
                strofa.append(['&' + new_line, u]) # добавляем к строфе вариантную строку
        s.append(strofa) # добавляем распарсенную строфу к тексту
    return dict(s=s, u=u, var_lines=var_lines, var_numbers=var_numbers, books = books, texts=texts)

def pun(line):
    l = ' '.join(line)
    l = l.replace(' ,', ',')
    l = l.replace(' .', ',')
    l = l.replace(' - ', '-')
    return l

def show_old(): # показываем текст в старой орфографии и параллельно в современной
    text = trymysql((trymysql.drafts.text==request.args(0))&(trymysql.drafts.book==request.args(1))).select().first()
    f = open(text.filename, 'rb')
    content = f.readlines()
    f.close()
    old_text = trymysql((trymysql.old.text==request.args(0))&(trymysql.old.book==request.args(1))).select().first()
    f1 = open(old_text.filename, 'rb')
    ocontent = f1.readlines()
    f1.close()
    return dict(text=text, old_text=old_text, content=content, ocontent=ocontent)

def show_page(): # показываем страницу книги, текст в оригинальной орфографии и текст в старой орфографии
    text = trymysql((trymysql.old.text==request.args(0))&(trymysql.old.book==request.args(1))).select().first()
    with open(text.filename, 'rb') as f:
        old = f.readlines()
    # page = trymysql((trymysql.page.text==request.args(0))&(trymysql.page.book==request.args(1))).select().first()
    u = 'books/' + str(request.args(1)) + '/' + text.book_page + '.png'
    book = request.args(1)
    new = trymysql((trymysql.drafts.text==request.args(0))&(trymysql.drafts.book==request.args(1))).select().first()
    with open(new.filename, 'rb') as f1:
        new = f1.readlines()
    return dict(old=old, new=new, text=text, u=u, book=book)

def show_book():
    book = trymysql(trymysql.biblio.id==request.args(0)).select()[0]
    pages = trymysql(trymysql.page.book==request.args(0)).select()
    texts = trymysql(trymysql.drafts.book==request.args(0)).select()
    old = trymysql(trymysql.old.book==request.args(0)).select()
    obl = 'books/' + str(book.id) + '/obl.png'
    drafts = []
    if len(old)==0:
        drafts = trymysql(trymysql.drafts.book==request.args(0)).select()
    return dict(book=book, pages=pages, texts=texts, old=old, obl=obl, drafts=drafts)
