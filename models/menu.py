# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('concor',SPAN('dances')),XML('.ru'),
                  _class="brand",_href="http://concordances.ru")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Maria Levchenko <marylevchenko@gmail.com>'
response.meta.keywords = 'concordance, natural language processing, critics'
response.meta.generator = 'Частотный словарь русской литературы'

## your http://google.com/analytics id
response.google_analytics_id = 'UA-52567545-1'

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
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
        (SPAN('web2py', _class='highlighted'), False, 'http://concordances.ru', [
        
        (T('О проекте'), False, URL('admin', 'default', 'about/' + app)),
        (T('Админка'), False, URL('admin', 'default', 'edit/%s/controllers/%s.py' % (app, ctr)))
      
            
           
           
                
                ]
         )]
if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu()
