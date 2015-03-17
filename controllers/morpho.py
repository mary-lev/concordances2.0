# coding: utf8
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

names = ['Abbr', 'Name', 'Surn', 'Patr', 'Geox', 'Init']
style = ['Infr', 'Slng', 'Arch', 'Litr', 'Erro', 'Dist']
other = ['Ques', 'Dmns', 'Prnt', 'Prdx', 'Af-p', 'Anph', 'Inmx', 'V-be', 'V-en', 'V-ie', 'V-bi', 'V-ey', 'V-oy', 'Cmp2', 'V-ej', 'Fimp', 'Coun', 'Coll', 'V-sh', 'Vpre', 'Supr', 'Qual', 'Apro', 'Anum', 'Poss']
partos = ['NOUN', 'ADJF', 'ADJS', 'VERB', 'INFN', 'GRND', 'PRTF', 'PRTS', 'ADVB', 'PREP', 'CONJ', 'NPRO', 'PRCL' ]
animacy = ['None','anim', 'inan']
gender = ['None','masc', 'femn', 'neut', 'Ms-f']
number = ['sing', 'plur', 'Sgtm', 'Pltm']
case = ['None','nomn', 'gent', 'datv', 'accs', 'ablt', 'loct', 'voct', 'gen1', 'gen2', 'acc2', 'loc1', 'loc2']
aspect = ['perf', 'impf']
trans = ['tran', 'intr']
person = ['1per', '2per', '3per']
tenses = ['past', 'pres', 'futr']
mood = ['indc', 'impr']
voice = ['actv', 'pssv']

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
        for all in case:
            count = trymysql((trymysql.allword.author==each)&(trymysql.allword.cas==all)).count()
            total = trymysql((trymysql.allword.author==each)&(trymysql.allword.cas!='None')).count()
            proc = round((float((count)*1.0)/int(total))*100, 3)
            result.append(proc)
        for all in partos:
            count = trymysql((trymysql.allword.author==each)&(trymysql.allword.partos==all)).count()
            total = trymysql((trymysql.allword.author==each)&(trymysql.allword.partos.belongs(partos))).count()
            proc = round((float((count)*1.0)/int(total))*100, 2)
            result.append(proc)
        for all in person:
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
    form=FORM(TABLE(TR("Часть речи",SELECT(*partos, _name="first")),
                    TR("Падеж",SELECT(*case, _name="second")),
                    TR("Одушевленность",SELECT(*animacy, _name="animacy")),
                    TR("Род", SELECT(*gender, _name="gender")),
                    TR("Автор", SELECT(*options2, _name="author")),
                    TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.process(formname='form_one').accepted:
        redirect(URL('search_result', args =
                     [form.vars['first'],
                      form.vars['second'],
                      form.vars['animacy'],
                      form.vars['gender'],
                      form.vars['author']]))
        response.flash="form accepted"
    return dict(form=form)

def search_result():
    selected_partos = request.args(0)
    selected_form = request.args(1)
    anim = request.args(2)
    gender = request.args(3)
    author = request.args(4)
    words = trymysql((trymysql.allword.partos==request.args(0))&
                     (trymysql.allword.anim==request.args(2))&
                     (trymysql.allword.gendr==request.args(3))&
                     (trymysql.allword.author==request.args(4))&
                     (trymysql.allword.cas==request.args(1))).select()
    strings =[]
    for all in words[:30]:
        location = all.text_location
        title1 = trymysql(trymysql.text1.id==int(all.title)).select()[0]
        title=title1.title
        author= (title1.author.name, title1.author.family)
        string="..."
        for x in range(all.id-6, all.id+6):
            for_string = trymysql(trymysql.allword.id==x).select()[0]
            string= string + " " + str(for_string.lemma)
        strings.append((string +"...", title, author, int(title1.id)))
    return dict(p = selected_partos, f = selected_form, strings=strings)
    
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
