# coding: utf8
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

names = ['None', 'Abbr', 'Name', 'Surn', 'Patr', 'Geox', 'Init']
style = ['Infr', 'Slng', 'Arch', 'Litr', 'Erro', 'Dist']
other = ['Ques', 'Dmns', 'Prnt', 'Prdx', 'Af-p', 'Anph', 'Inmx', 'V-be', 'V-en', 'V-ie', 'V-bi', 'V-ey', 'V-oy', 'Cmp2', 'V-ej', 'Fimp', 'Coun', 'Coll', 'V-sh', 'Vpre', 'Supr', 'Qual', 'Apro', 'Anum', 'Poss']

partos = ['None', 'NOUN', 'ADJF', 'ADJS', 'VERB', 'INFN', 'GRND', 'PRTF', 'PRTS', 'ADVB', 'PREP', 'CONJ', 'NPRO', 'PRCL' ]
animacy = ['None','anim', 'inan']
gender = ['None','masc', 'femn', 'neut', 'Ms-f']
number = ['None', 'sing', 'plur', 'Sgtm', 'Pltm']
case = ['None','nomn', 'gent', 'datv', 'accs', 'ablt', 'loct', 'voct', 'gen1', 'gen2', 'acc2', 'loc1', 'loc2']
aspect = ['None', 'perf', 'impf']
trans = ['None', 'tran', 'intr']
person = ['None', '1per', '2per', '3per']
tenses = ['None', 'past', 'pres', 'futr']
mood = ['None', 'indc', 'impr']
voice = ['None', 'actv', 'pssv']

def index():
    authors = trymysql().select(trymysql.author.ALL, orderby=trymysql.author.id)
    return dict(authors=authors)

def index1():
    titles = [x for x in range(3335,3500)]
    texts = trymysql(trymysql.allword.title.belongs(titles)).select()
    for all in texts:
        the_word = all.lemma.decode("utf-8")
        normal = morph.parse(the_word)[0]
        parsed_other = parse_tags(normal.tag, other)['result']
        parsed_style = parse_tags(normal.tag, style)['result']
        parsed_name = parse_tags(normal.tag, names)['result']
        if all.partos != 'None' and all.partos != 'PNCT':
            all.update_record(anim = str(normal.tag.animacy), gendr=str(normal.tag.gender), number = str(normal.tag.number), cas = str(normal.tag.case), tense = str(normal.tag.tense), aspect = str(normal.tag.aspect), person = str(normal.tag.person), transitivity= str(normal.tag.transitivity), mood = str(normal.tag.mood), involvment = str(normal.tag.involvement), voice = str(normal.tag.voice), sobstv=parsed_name, style = parsed_style, other = parsed_other)
    return dict(parsed_other=parsed_other)

def parse_tags(tags, list_tags):
    parsed = [x for x in list_tags if x in tags]
    result = 'None'
    for all in parsed:
        if all != 'None':
            result = str(all)
    return dict(result=result)

def count_partos(): # count categories by author
    new = []
    authors = [1,4,5,7,8,9,10,11, 12]
    for each in authors:
        family = trymysql(trymysql.author.id==each).select()[0]
        result = [family['family']]
        for all in case[1:]:
            count = trymysql((trymysql.allword.author==each)&(trymysql.allword.cas==all)).count()
            total = trymysql((trymysql.allword.author==each)&(trymysql.allword.cas!='None')).count()
            proc = round((float((count)*1.0)/int(total))*100, 3)
            result.append(proc)
        for all in partos[1:]:
            count = trymysql((trymysql.allword.author==each)&(trymysql.allword.partos==all)).count()
            total = trymysql((trymysql.allword.author==each)&(trymysql.allword.partos.belongs(partos))).count()
            proc = round((float((count)*1.0)/int(total))*100, 2)
            result.append(proc)
        for all in person[1:]:
            count = trymysql((trymysql.allword.author==each)&(trymysql.allword.person==all)).count()
            total = trymysql((trymysql.allword.author==each)&(trymysql.allword.person!='None')).count()
            proc = round((float((count)*1.0)/int(total))*100, 2)
            result.append(proc)
        new.append(result)
    new_tense = []
    for every in authors:
        family = trymysql(trymysql.author.id==every).select()[0]
        total = trymysql((trymysql.allword.author==every)&(trymysql.allword.tense!='None')).count()
        tense = [round(float(trymysql((trymysql.allword.author==every)&(trymysql.allword.tense==all)).count())*1.0/int(total)*100,2) for all in tenses]
        new_tense.append((family['family'],tense))
    return dict(new=new, new_tense=new_tense)

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

def search():
    options2 = [OPTION(texts.name, " ", texts.family, _value=texts.id) for texts in trymysql().select(trymysql.author.ALL)]
    form=FORM(TABLE(TR("Автор", SELECT(*options2, _name="author")),
                    TR("Часть речи",SELECT(*partos, _name="first")),
                    TR("Падеж",SELECT(*case, _name="second")),
                    TR("Одушевленность",SELECT(*animacy, _name="animacy")),
                    TR("Род", SELECT(*gender, _name="gender")),
                    TR("Время", SELECT(*tenses, _name="tenses")),
                    TR("Вид", SELECT(*aspect, _name = "aspect")),
                    TR("Залог", SELECT(*voice, _name = "voice")),
                    TR("Лицо", SELECT(*person, _name = "person")),
                    TR("Переходность", SELECT(*trans, _name = "trans")),
                    TR("Число", SELECT(*number, _name = "number")),
                    TR("Наклонение", SELECT(*mood, _name="mood")),
                    TR("Имена собственные", SELECT(*names, _name="names")),
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
    words = trymysql(trymysql.allword.author==request.args(4)).select(trymysql.allword.id)
    if request.args(0) != 'None':
        words = trymysql((trymysql.allword.id.belongs(words))&(trymysql.allword.partos==request.args(0))).select()
    if request.args(1) != 'None':
        words = trymysql((trymysql.allword.id.belongs(words))&(trymysql.allword.cas==request.args(1))).select()
    if request.args(2) != 'None':
        words = trymysql((trymysql.allword.id.belongs(words))&(trymysql.allword.anim==request.args(2))).select()
    if request.args(3) != 'None':
        words = trymysql((trymysql.allword.id.belongs(words))&(trymysql.allword.gendr==request.args(3))).select()
    if request.args(5) != 'None':
        words = trymysql((trymysql.allword.id.belongs(words))&(trymysql.allword.tense==request.args(5))).select()
    if request.args(6) != 'None':
        words = trymysql((trymysql.allword.id.belongs(words))&(trymysql.allword.aspect==request.args(6))).select()
    if request.args(7) != 'None':
        words = trymysql((trymysql.allword.id.belongs(words))&(trymysql.allword.voice==request.args(7))).select()
    if request.args(8) != 'None':
        words = trymysql((trymysql.allword.id.belongs(words))&(trymysql.allword.person==request.args(8))).select()
    if request.args(9) != 'None':
        words = trymysql((trymysql.allword.id.belongs(words))&(trymysql.allword.transitivity==request.args(9))).select()
    if request.args(10) != 'None':
        words = trymysql((trymysql.allword.id.belongs(words))&(trymysql.allword.number==request.args(10))).select()
    if request.args(11) != 'None':
        words = trymysql((trymysql.allword.id.belongs(words))&(trymysql.allword.mood==request.args(11))).select()
    if request.args(12) != 'None':
        words = trymysql((trymysql.allword.id.belongs(words))&(trymysql.allword.sobstv==request.args(12))).select()
    message=""
    strings=[]
    if len(words) == 0:
        message = "Sorry, nothing found"
    else:
        for all in words:
            location = all.text_location
            title1 = trymysql(trymysql.text1.id==int(all.title)).select()[0]
            title=title1.title
            author= (title1.author.name, title1.author.family)
            string="..."
            for x in range(all.id-6, all.id+6):
                try:
                    for_string = trymysql(trymysql.allword.id==x).select()[0]
                    string= string + " " + str(for_string.lemma)
                except:
                    pass
            strings.append((string +"...", title, author, int(title1.id)))
    return dict(strings=strings, message=message)

def draft():
    base_id=[int(all.id) for all in trymysql(trymysql.text1.group_text==request.args(0)).select()]
    base_id0=[int(all.id) for all in trymysql(trymysql.text1.group_text==request.args(1)).select()]
    colours=[trymysql((trymysql.allword.word==all)&(trymysql.allword.title.belongs(base_id))).count() for all in color]
    colours2=[trymysql((trymysql.allword.word==all)&(trymysql.allword.title.belongs(base_id0))).count() for all in color]
    all_colours = sum([int(x) for x in colours])
    all_colours2 = sum([int(x) for x in colours2])
    title_1 = trymysql(trymysql.group_text.id==request.args(0)).select().first()
    title_2 = trymysql(trymysql.group_text.id==request.args(1)).select().first()
    return dict(colours=colours, colours2=colours2, all_colours=all_colours, all_colours2=all_colours2, title1=title_1.title, author1=title_1.author.family, title2=title_2.title, author2=title_2.author.family)
