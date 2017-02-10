# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
from datetime import date

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

def index():
    texts = trymysql(trymysql.author.id!='23').select(orderby=trymysql.author.family)

    # Блок "Сегодня написаны тексты"
    numbers = []
    n = 0
    today = date.today()
    m = months[today.month-1]
    if today.month < 10:
        month = '0' + str(today.month)
    else:
        month = str(today.month)
    day = trymysql((trymysql.text1.month_writing==month)&(trymysql.text1.day_writing==today.day)).select(orderby=trymysql.text1.year_writing)
    for all in texts:
        number = trymysql(trymysql.text1.author==all.id).count()
        numbers.append([all.name, all.family,all.id, number])
        n += number

    ex = ['5', '7', '10', '11', '17'] # исключаем не-книжки из блока "Издания"
    books = trymysql(~trymysql.biblio.id.belongs(ex)).select(orderby=trymysql.biblio.short)
    return dict(texts=texts, numbers=numbers, n = n, day=day, d = today.day, m = m, books=books)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
