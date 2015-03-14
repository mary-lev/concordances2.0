# coding: utf8
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

names = ['Abbr', 'Name', 'Surn', 'Patr', 'Geox', 'Init']
style = ['Infr', 'Slng', 'Arch', 'Litr', 'Erro', 'Dist']
other = ['Ques', 'Dmns', 'Prnt', 'Prdx', 'Af-p', 'Anph', 'Inmx', 'V-be', 'V-en', 'V-ie', 'V-bi', 'V-ey', 'V-oy', 'Cmp2', 'V-ej', 'Fimp', 'Coun', 'Coll', 'V-sh', 'Vpre', 'Supr', 'Qual', 'Apro', 'Anum', 'Poss']
partos = ['NOUN', 'ADJF', 'ADJS', 'VERB', 'INFN', 'GRND', 'PRTF', 'PRTS', 'ADVB', 'PREP', 'CONJ', 'NPRO', 'PRCL' ]
animacy = ['anim', 'inan']
gender = ['masc', 'femn', 'neut', 'Ms-f']
number = ['sing', 'plur', 'Sgtm', 'Pltm']
case = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct', 'voct', 'gen1', 'gen2', 'acc2', 'loc1', 'loc2']
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
    titles = [x for x in range(3292,3335)]
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

def visual():
    return dict()
