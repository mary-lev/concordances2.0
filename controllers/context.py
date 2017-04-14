# coding: utf8

def index(): # get text from user's file
    form = SQLFORM.factory(Field('word')).process()
    if form.accepted:
        redirect(URL('context', vars = form.vars))
    return dict(form=form)

def context1():
    text1 = request.vars.word
    texts = trymysql(trymysql.allword.word==request.vars.word).select()
    strings=[]
    for all in texts:
        location = all.text_location
        title1 = trymysql(trymysql.text1.id==int(all.title)).select()[0]
        title=title1.title
        author= (title1.author.name, title1.author.family)
        string="..."
        for x in range(all.id-6, all.id+6):
            try:
                for_string = trymysql(trymysql.allword.id==x).select()[0]
                if for_string.lemma=="," or for_string.lemma=='.' or for_string.lemma=='!':
                    string = string + str(for_string.lemma)
                else:
                    string= string + " " + str(for_string.lemma)
            except:
                pass
        strings.append((string +"...", title, author, int(title1.id)))
    return dict(strings=strings)

def context():
    text1 = request.vars.word
    texts = trymysql(trymysql.mystem.word==request.vars.word).select()
    if len(texts)==0:
        word = text1+'?'
        texts = trymysql(trymysql.mystem.word==word).select()
    strings=[]
    for all in texts:
        location = all.location
        title1 = trymysql(trymysql.text1.id==int(all.title)).select()[0]
        title=title1.title
        author= (title1.author.name, title1.author.family)
        with open(title1.filename, 'r') as f:
            content = f.readlines()
            string = content[int(all.location)-1]
            all_string_words = [[w.lemma, w.id] for w in trymysql((trymysql.mystem.title==all.title)&(trymysql.mystem.location==all.location)).select()]
            color_string = []
            for lemma in all_string_words:
                if lemma[1] == all.id:
                    color_word = '&' + lemma[0]
                    color_string.append(color_word)
                else:
                    color_string.append(lemma[0])
        strings.append((' '.join(color_string) +"...", title, author, int(title1.id)))
    return dict(strings=strings)
