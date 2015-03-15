# coding: utf8
# попробовать что-либо вида

def show1():   # show text from file
    texts = trymysql(trymysql.text1.id==request.args(0)).select().first()
    f = open(texts.filename, 'rb')
    content = f.readlines()
    return dict(texts=texts, content=content)

def show2(): # color the verbs
    words = trymysql(trymysql.allword.title==request.args(0)).select()
    content = []
    for row in words:
        if row.partos=='VERB':
            new_words=str(row.lemma)+str('&')
            content.append(new_words)
        else:
            content.append(row.lemma)
    return dict(content=content)

def show3():
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
