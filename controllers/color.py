# coding: utf8
from __future__ import division

color=["зелёный", "золотой", "голубой", "красный", "белый", "жёлтый", "чёрный", "коричневый", "синий", "розовый", "пурпурный", "фиолетовый", "серый", "жолтый", "лазурный", "алый", "лазоревый", "синева", "золотистый", "рыжий", "голубоватый", "златой", "бирюзовый", "лазурь", "бирюза", "пурпуровый", "чернеть", "белеть"]

color2=["зеленый", "золото", "голубой", "красный", "белый", "желтый", "черный", "коричневый", "синий", "розовый", "пурпур", "фиолетовый", "серый", "лазурь", "алый", "рыжий", "бирюза", 'оранжевый', 'багровый', 'багряный', 'лиловый', 'сирень', 'сизый', 'серебро']

colorfile = '/home/concordance/web2py/applications/test/corpus/colors.txt'

def index():
    with open(colorfile, 'r') as f:
        data = f.readlines()

    # считаем сумму каждого цвета для всего корпуса из файла
    ints = [[int(a) for a in i.split(',')] for i in data] # переводим все в цифры
    colours2 = [sum(i) for i in zip(*ints)] # складываем последовательно количества каждого цвета
    colours2.pop(0) # убираем первый элемент списка (id авторов)
    all_words = colours2.pop(-1) # выбираем последний элемент списка - сумма всех слов всех авторов
    all_colours = sum(colours2) # считаем количество цветообозначений
    proc = round(float(all_colours)/float(all_words) * 100, 3) # считаем процент цветообозначений

    # считаем процент цвета для каждого автора
    new_data = [a.split(',') for a in data] # готовим к подсчету авторского процента цветообозначений
    au_pro = [] # это будет список индивидуальных авторских процентов
    auts = []
    for all in new_data:
        s = all.pop(0)
        auts.append(s)
        words = int(all.pop(-1))
        all_col = sum([int(a) for a in all])
        pro = round(float(all_col)/float(words)*100, 2)
        au_pro.append(pro)
    average_pro = round(sum(au_pro) / len(au_pro), 3) # средний процент цвета у авторов корпуса

    authors = trymysql().select(trymysql.author.ALL) # все авторы
    options = [OPTION(texts.title, _value=texts.id) for texts in trymysql().select(trymysql.group_text.ALL)]
    form=FORM(TABLE(TR("Выберите первый текст",SELECT(*options, _name="first")),
                    TR("Выберите второй текст",SELECT(*options, _name="second")),
                    TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.process(formname='form_one').accepted:
        redirect(URL('image_compare', args = [form.vars['first'], form.vars['second']]))
        response.flash="form accepted"
    options2 = [OPTION(texts.name, " ", texts.family, _value=texts.id) for texts in trymysql().select(trymysql.author.ALL)]
    form2=FORM(TABLE(TR("Выберите первый текст",SELECT(*options2, _name="first1")),
                    TR("Выберите второй текст",SELECT(*options2, _name="second1")),
                    TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form2.process(formname='form_two').accepted:
        redirect(URL('author_compare', args = [form2.vars['first1'], form2.vars['second1']]))
        response.flash="form accepted"
    return dict(colours2=colours2, all_colours=all_colours, all_words=all_words, authors=authors, auts=auts, form=form, form2=form2, proc=proc, average_pro = average_pro, au_pro = au_pro)

def index1():
    authors = trymysql().select(trymysql.author.ALL)
    a = d((d.mystem.partos!="None")&(d.mystem.partos!='PNCT')).count()
    new_colors = []
    count = []
    darkwords = [w.pro for w in trymysql(trymysql.slovar1.word=='тьма').select()]
    lightwords = [w.pro for w in trymysql(trymysql.slovar1.word=='свет').select()]
    dark = d(d.mystem.word.belongs(darkwords)).count()
    light = d(d.mystem.word.belongs(lightwords)).count()
    for all in color2:
        all_words = [w.pro for w in trymysql(trymysql.slovar1.word==all).select()]
        all_words.append(all)
        new_colors.append(' '.join(set(all_words)))
        summa = d(d.mystem.word.belongs(all_words)).count()
        count.append(summa)
    return dict(new_colors = new_colors, colours=count, m = sum(count), authors=authors, a=a, dark=dark, light=light)

def author(): # отображение данных по цветообозначениям из файла
    author1=trymysql(trymysql.author.id==request.args(0)).select()[0]
    with open(colorfile, 'r') as f:
        data = f.readlines()
    for all in data:
        all = all.split(',')
        if all[0] == str(author1.id):
            all.pop(0) # убираем id автора из строки
            all_words2 = int(all.pop(-1)) # выбираем общее количество слов в корпусе автора из строки (последнее число)
            colours2 = [int(d) for d in all]
    proc = round(float(sum(colours2))/float(all_words2) * 100, 3)
    authors = trymysql().select(trymysql.author.ALL) # все авторы
    return dict(colours2=colours2, all_words2=all_words2, author=author1, authors=authors, proc=proc)

def author_all_color():
    author1=trymysql(trymysql.author.id==request.args(0)).select()[0]
    authors = trymysql().select(trymysql.author.ALL)
    result = []
    #test_words = ['сизый']
    for all in color2:
        color_list = []
        pros = [p.pro for p in trymysql(trymysql.slovar1.word==all).select()]
        pros.append(all)
        rows = d((d.mystem.word.belongs(pros))&(d.mystem.author==request.args(0))).select()
        for r in rows:
            filename = '/home/concordance/web2py/applications/test/corpus/' + str(request.args(0)) + '/' + str(r.title) + '.txt'
            with open(filename, 'rb') as f:
                text = f.readlines()
            corpus_text = text[int(r.location)-1]
            text = trymysql(trymysql.text1.id == r.title).select()[0]
            color_list.append([corpus_text, text])
        result.append([all, color_list])
    return dict(text=result, author = author1, authors=authors)

@auth.requires_login()
def author_index(): # сохраняем авторские данные в текстовый файл для ускорения рисования кружочков
    author1=trymysql(trymysql.author.id==request.args(0)).select()[0]
    result=[str(author1.id)]
    for all in color2:
        all_word = [w.pro for w in trymysql(trymysql.slovar1.word==all).select()]
        all_word.append(all)
        summa = d((d.mystem.word.belongs(all_word))&(d.mystem.author==request.args(0))).count()
        result.append(str(summa))
    all_words2 = d((d.mystem.author==request.args(0))&(d.mystem.partos!='None')).count()
    result.append(str(all_words2))
    result = ','.join(result) + '\n'
    with open(colorfile, 'a') as f:
        f.write(result)
    return dict(message=result)

def image_compare(): # Сравниваем цвета двух текстов
    base_id=[int(all.id) for all in trymysql(trymysql.text1.group_text==request.args(0)).select()]
    base_id0=[int(all.id) for all in trymysql(trymysql.text1.group_text==request.args(1)).select()]
    colours=[trymysql((trymysql.allword.word==all)&(trymysql.allword.title.belongs(base_id))).count() for all in color]
    colours2=[trymysql((trymysql.allword.word==all)&(trymysql.allword.title.belongs(base_id0))).count() for all in color]
    all_colours = sum([int(x) for x in colours])
    all_colours2 = sum([int(x) for x in colours2])
    title_1 = trymysql(trymysql.group_text.id==request.args(0)).select().first()
    title_2 = trymysql(trymysql.group_text.id==request.args(1)).select().first()
    return dict(colours=colours, colours2=colours2, all_colours=all_colours, all_colours2=all_colours2, title1=title_1.title, author1=title_1.author.family, title2=title_2.title, author2=title_2.author.family)

def author_compare(): # Сравниваем цвета двух авторов
    with open(colorfile, 'r') as f:
        data = f.readlines()
    data = [all.split(',') for all in data]
    for all in data:
        l = all.pop(0)
        if int(l)==int(request.args(0)):
            c1 = all.pop(-1)
            colours = all
        elif int(l)==int(request.args(1)):
            c2 = all.pop(-1)
            colours2 = all
    #colours=[trymysql((trymysql.allword.word==all)&(trymysql.allword.author==request.args(0))).count() for all in color]
    #colours2=[trymysql((trymysql.allword.word==all)&(trymysql.allword.author==request.args(1))).count() for all in color]
    all_colours = sum([int(x) for x in colours])
    all_colours2 = sum([int(x) for x in colours2])
    author1 = trymysql(trymysql.author.id==request.args(0)).select().first()
    author2 = trymysql(trymysql.author.id==request.args(1)).select().first()
    return dict(colours=colours, colours2=colours2, all_colours=all_colours, all_colours2=all_colours2, c1 = c1, c2=c2, author1=author1, author2=author2)

imemines = ["я", "мой", "мы", "себя", "ты", "твой", "он", "она", "они"]

def imemine():
    mine = [trymysql((trymysql.allword.word==all)&(trymysql.allword.author==request.args(0))).count() for all in imemines]
    author1=trymysql(trymysql.author.id==request.args(0)).select()[0]
    author=author1['family']
    return dict(mine=mine, all_mine=mine, author=author)

months = ['январь', 'январский', 'февраль', 'февральский', 'март', 'мартовский', 'апрель', 'апрельский', 'май', 'майский', 'июнь', 'июньский', 'июль', 'июльский', 'август', 'августовский', 'сентябрь', 'сентябрьский', 'октябрь', 'октябрьский', 'ноябрь', 'ноябрьский', 'декабрь', 'декабрьский']

def month():
    colours=[trymysql((trymysql.allword.word==all)&(trymysql.allword.author==request.args(0))).count() for all in months]
    all_colours = sum([int(x) for x in colours])
    all = trymysql((trymysql.allword.partos!="None")&(trymysql.allword.author==request.args(0))).count()
    author1=trymysql(trymysql.author.id==request.args(0)).select()[0]
    author=author1['family']
    return dict(colours=colours, all_colours=all_colours, all=all, author=author)

season = ['зима', 'зимний', 'весна', 'весенний', 'лето', 'летний', 'осень', 'осенний']

def seasons():
    colours=[trymysql((trymysql.allword.word==all)&(trymysql.allword.author==request.args(0))).count() for all in season]
    all_colours = sum([int(x) for x in colours])
    all = trymysql((trymysql.allword.partos!="None")&(trymysql.allword.author==request.args(0))).count()
    author1=trymysql(trymysql.author.id==request.args(0)).select()[0]
    author=author1['family']
    return dict(colours=colours, all_colours=all_colours, all=all, author=author)
