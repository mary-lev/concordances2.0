# coding: utf8

from random import gauss
from math import sin, cos
from canvas import Canvas

def index():
    return dict(message="hello from pic.py")

def my_image():
    points=[(x,x+gauss(0,1),0.5) for x in range(20)]
    response.headers['Content-type'] = 'image/png'
    return Canvas('Title').errorbar(points).plot(points).binary()
