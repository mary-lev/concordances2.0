# coding: utf8
# попробовать что-либо вида

def index():
    #all_epi = trymysql(trymysql.text1.epigraph!='').select()
    all_authors = trymysql(trymysql.epi.id>0).select(groupby=trymysql.epi.epi_author)
    maxID=trymysql(trymysql.text1).select(trymysql.text1.id.max()).first()[trymysql.text1.id.max()]
    return dict(all_epi=all_authors, maxID=maxID)
