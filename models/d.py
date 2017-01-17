# coding: utf8
d = DAL('mysql://concordance:sosnora@concordance.mysql.pythonanywhere-services.com/concordance$try')

d.define_table('stress',
               Field('lemma', label = "Начальная форма"),
               Field('form', label = "Слово"),
               Field('stress', label = "Слово с ударением"))

d.define_table('pages',
               Field('author', label = "Автор"),
               Field('edition', label = "Издание"),
               Field('text', label = "Текст"),
               Field('page_number', label = "Страница"),
               Field('url', label = "Url"))
