# coding: utf8

def index():
    geo = trymysql(trymysql.allword.sobstv=='GEOX').select()
    geotag = [all.word for all in geo]
    geotag = sorted(set(geotag))
    return dict(geotag=geotag)
