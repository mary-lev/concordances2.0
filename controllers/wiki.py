import xml.etree.ElementTree as ET
from urllib import urlopen
import mw
import json
from wikitools import wiki
from wikitools import api

stress= "е́, ы́, а́, о́, э́, я́́, и́, ю́, у́"

def index1():
    # create a Wiki object
    site = wiki.Wiki("http://ru.wiktionary.org/w/api.php")
    # login - required for read-restricted wikis
    # site.login("Maryl", "sosnora")
    # define the params for the query
    params = {'action':'query', 'titles':'Роза', }
    # create the request object
    request = api.APIRequest(site, params)
    # query the API
    result = request.query()
    return dict(result=result)


def index():
    word = "аист"
    url = "http://ru.wiktionary.org/wiki/" + word + "?action=raw"
    text = urlopen(url).readlines()
    text1 = urlopen(url).read()
    new4= ""
    rod1=''
    for line in text:
        if "слоги" in line:
            new = line
            new1 = new.find('слоги')
            new2=new[new1:]
            new3=new2.find("|")
            new4=new2[new3+1:-3]
    rodstv = "=== Родственные слова ==="
    if rodstv in text1:
        rod = text1.find("=== Родственные слова ===")
        end1 = "=="
        rod1 = text1[rod+41:]
        end = rod1.find("Этимология")
        rod2 = rod1[:end-4]
    t = type(text)
    return dict(text=text, new4=new4, rod2=rod2, a = stress)

def index2():
    enwp = mw.Wiki('https://ru.wiktionary.org/w/api.php')
    #nwp.login('maryl', 'sosnora')
    #https://en.wikipedia.org/w/api.php?action=query&meta=userinfo&uiprop=hasmsg&format=jsonfm
    params = {'action':'query',
              'titles':'Роза',
              'rvprop':'content',
              'prop':'revisions',
              'redirects':'1'
              }
    data = enwp.request(params)
    data1 = data['query']['pages']
    #data_new = [all for all in data1]
    #data2=data['query']['pages'][data_new[0]]['revisions'][0]
    #c=[all[0] for all in data2][0]
    #data_new2 = data2[c]
    #t = type(data)
    return dict(data1=data1)
