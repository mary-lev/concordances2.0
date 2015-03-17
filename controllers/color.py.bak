# coding: utf8

color=["зелёный", "золотой", "голубой", "красный", "белый", "жёлтый", "чёрный", "коричневый", "синий", "розовый", "пурпурный", "фиолетовый", "серый", "жолтый", "лазурный", "алый", "лазоревый", "синева", "золотистый", "рыжий", "голубоватый", "златой", "бирюзовый", "лазурь", "бирюза", "пурпуровый", "чернеть", "белеть"]

imemines = ["я", "мой", "меня", "мы", "себя", "ты", "тебя", "твой", "он", "она", "они"]

def index():
    colours=[trymysql(trymysql.allword.word==all).count() for all in color]
    all_colours = sum([int(x) for x in colours])
    all = trymysql(trymysql.allword.partos!="None").count()
    authors = trymysql().select(trymysql.author.ALL)
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
    return dict(colours=colours, all_colours=all_colours, all=all, authors=authors, form=form, form2=form2)

def author():
    colours=[trymysql((trymysql.allword.word==all)&(trymysql.allword.author==request.args(0))).count() for all in color]
    all_colours = sum([int(x) for x in colours])
    all = trymysql((trymysql.allword.partos!="None")&(trymysql.allword.author==request.args(0))).count()
    author1=trymysql(trymysql.author.id==request.args(0)).select()[0]
    author=author1['family']
    return dict(colours=colours, all_colours=all_colours, all=all, author=author)

def author_index(): # форма для выбора двух текстов, передает id текста для операци сравнения лексики (compare)
    options2 = [OPTION(texts.name, " ", texts.family, _value=texts.id) for texts in trymysql().select(trymysql.author.ALL)]
    form=FORM(TABLE(TR("Выберите первый текст",SELECT(*options2, _name="first1")),
                    TR("Выберите второй текст",SELECT(*options2, _name="second1")),
                    TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.process(formname='form_two').accepted:
        redirect(URL('author_compare', args = [form.vars['first1'], form.vars['second1']]))
        response.flash="form accepted"
    return dict(form=form)

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
    colours=[trymysql((trymysql.allword.word==all)&(trymysql.allword.author==request.args(0))).count() for all in color]
    colours2=[trymysql((trymysql.allword.word==all)&(trymysql.allword.author==request.args(1))).count() for all in color]
    all_colours = sum([int(x) for x in colours])
    all_colours2 = sum([int(x) for x in colours2])
    author1 = trymysql(trymysql.author.id==request.args(0)).select().first()
    author2 = trymysql(trymysql.author.id==request.args(1)).select().first()
    return dict(colours=colours, colours2=colours2, all_colours=all_colours, all_colours2=all_colours2, author1=author1.family, author2=author2.family)

def imemine():
    mine = [trymysql((trymysql.allword.word==all)&(trymysql.allword.author=='1')).count() for all in imemines]
    return dict(mine=mine, all_mine=mine)

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
