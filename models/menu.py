# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('concor',SPAN('dances')),XML('.ru'),
                  _class="brand",_href="http://concordance.pythonanywhere.com")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Maria Levchenko <marylevchenko@gmail.com>'
response.meta.keywords = 'concordance, natural language processing, russian poetry'
response.meta.generator = 'Частотный словарь русской литературы'

## your http://google.com/analytics id
response.google_analytics_id = 'UA-52567545-1'

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'index'), [
    (T('Админка'), False, URL('admin', 'default', 'edit/test'))])
]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu += [
        (SPAN('Корпус', _class='highlighted'), False, '', [
        (T('Александр Блок'), False, URL('author', 'all_author', args='1')),
        (T('Николай Гумилев'), False, URL('author', 'all_author', args='2')),
        (T('Осип Мандельштам'), False, URL('author', 'all_author', args='4')),
        (T('Андрей Белый'), False, URL('author', 'all_author', args='5')),
        (T('Иннокентий Анненский'), False, URL('author', 'all_author', args='7')),
        (T('Валерий Брюсов'), False, URL('author', 'all_author', args='8')),
        (T('Борис Пастернак'), False, URL('author', 'all_author', args='9')),
        ]),

        (SPAN('Цвета', _class='highlighted'), False, URL('color', 'index'), [
        (T('В корпусе'), False, URL('color', 'index')),
        (T('Цветовая близость'), False, URL('color', 'vis')),
        (T('Александр Блок'), False, URL('color', 'author', args='1')),
        (T('Николай Гумилев'), False, URL('color', 'author', args='2')),
        (T('Осип Мандельштам'), False, URL('color', 'author', args='4')),
        (T('Андрей Белый'), False, URL('color', 'author', args='5'))
         ]          ),

        (SPAN('Поиск', _class='highlighted'), False, 'http://concordances.ru', [
        (T('Контекстный поиск'), False, URL('context', 'index')),
        (T('Морфологический поиск'), False, URL('morpho', 'search'))       ] ),

        (SPAN('Конкорданс', _class='highlighted'), False, URL('concordance', 'conc') ),

        (SPAN('Статистика', _class='highlighted'), False, URL('count', 'index'), [
        (T('Части речи'), False, URL('count', 'index')),
        ] ),

        (SPAN('Векторная модель', _class='highlighted'), False, URL('concordance', 'model'), [
        (T('Поиск слова'), False, URL('concordance', 'ask_model')),
        (T('Животные'), False, URL('concordance', 'zveri')),
        (T('Птицы'), False, URL('concordance', 'birds')),
        ] ),
        (SPAN('Заточник', _class='highlighted'), False, URL('zatochnik', 'index'))
         ]

if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu()
