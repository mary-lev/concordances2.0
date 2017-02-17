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

d.define_table('mystem',
               Field('word', label="Слово"),
               Field('title', label="Текст"),
               Field('partos', label="Часть речи"),
               Field('anim', label="Одушевленность"),
               Field('gender', label="Род"),
               Field('forma', label = "Форма"),
               Field('comp', label = "Сравнит"),
               Field('number', label="Число"),
               Field('cas', label="Падеж"),
               Field('tense', label="Время"),
               Field('aspect', label="Вид"),
               Field('person', label="Лицо"),
               Field('trans', label="Переходность"),
               Field('verb', label="Форма глагола"),
               Field('voice', label="Залог"),
               Field('other', label="Другое"),
               Field('lexical_group', label="Лексическая группа"),
               Field('location', label='Номер в тексте'),
               Field('concordance_number',  label="Номер в конкордансе"),
               Field('author', label="Автор") )
