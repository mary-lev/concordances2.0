# coding: utf8
# попробовать что-либо вида

def show1():   # show text from file
    texts = trymysql(trymysql.text1.id==request.args(0)).select().first()
    f = open(texts.filename, 'rb')
    content = f.readlines()
    image = [all.url for all in d(d.pages.text==request.args(0)).select()]
    return dict(texts=texts, content=content, image=image)

def show2(): # color the verbs
    text = trymysql(trymysql.text1.id==481).select()[0]
    words_numbers = [all.id for all in trymysql(trymysql.allword.title==text.id).select()]
    f = open(text.filename, 'rb')
    content = f.readlines()
    f.close()
    var = trymysql(trymysql.variants.title==text.id).select()
    line_number = [a.line for a in var]
    word = [a.comment_text for a in var]
    varbook = [a.comment_book for a in var]

    return dict(text=text, content = content, line_number = line_number, word=word, varbook = varbook)

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

def show_variants(): # doesn't work
    texts = trymysql(trymysql.text1.id==request.args(0)).select().first()
    filename = "/home/concordance/web2py/applications/test/uploads/xml//4/481.xml"
    f = open(filename, 'rb')
    content = f.read()
    #if texts.id in [all.title for all in trymysql(trymysql.variants.id>0).select()]:
    #    word = trymysql(trymysql.variants.title==texts.id).select().first()
     #   word=word['comment_text']
    return dict(content=content)
