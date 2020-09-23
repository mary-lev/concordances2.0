# coding: utf8
import requests
import json

def index():
    geotag = trymysql((trymysql.text1.writing_location!= None)&(trymysql.text1.writing_location!='')).select()
    geo = [[all.id, all.writing_location, all.year_writing] for all in geotag]
    with open('location.json', 'w') as f:
        json.dump(geo, f)
    #geotag = sorted(set(geo))

    return dict(geotag=geotag)

def index1():
    geo = trymysql(trymysql.allword.sobstv=='GEOX').select()
    geotag = [all.word for all in geo]
    geotag = sorted(set(geotag))
    return dict(geotag=geotag)

def find_geo_coor():
    google = []
    for all in geotag[:50]:
        coor = get_coor(all)
        google.append([all, coor])
    return dict(google=google)

def get_coor(req):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'sensor': 'false', 'address': req}
    r = requests.get(url, params=params)
    results = r.json()['results']
    return results
