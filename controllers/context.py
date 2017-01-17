# coding: utf8

def index(): # get text from user's file
    form = SQLFORM.factory(Field('word')).process()
    if form.accepted:
        redirect(URL('context1', vars = form.vars))
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
