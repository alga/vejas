#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  muller.py

  Process GFS wind forecasts (http://www.wetterzentrale.de/)

$Id: muller.py,v 1.20 2005/07/19 10:40:28 alga Exp $
"""

import sys
import urllib
import time
import datetime
import os.path
from PIL import Image
from cStringIO import StringIO
from zope.pagetemplate.pagetemplatefile import PageTemplateFile

dirname = os.path.dirname(__file__)
outputdir = "."


def rect(x, y, w, h):
    return (x, y, x + w, y + h)


class WindPicture:
    """Vėjo paveiksliuko gavimas/apdorojimas"""

    url = "http://www.wetterzentrale.de/pics/Rtavn%s9.gif"
    maskName = os.path.join(dirname, "crop-map.png")
    map =   rect(520, 62, 214, 158)
    mapoffset = (20, 0)
    date =  rect(536, 5, 257, 16)
    scale = rect(800, 100, 35, 489)
    newDate = (214, 14)
    dateOffset = (0, 0)
    mapOffset = (0, 14)

    canvasSize = (214, 172)

    def __init__(self, hr=None, file=None):
        if hr:
            url = self.url % hr
            data = urllib.urlopen(url)
            file = StringIO(data.read())
        if type(file) == type(""):
            file = open(file)
        self.pic = Image.open(file)
        #self.mask = Image.open(self.maskName)

    def getMap(self):
        "Iškerpa reikalingą gabalą ir užpaišo Lietuvą"
        map = self.pic.crop(self.map)
        map = map.convert("RGB")
        #map.paste(self.mask, self.mapoffset, self.mask)
        return  map

    def getDate(self):
        "Iškerpa datą"
        pic = self.pic.crop(self.date)
        pic = pic.convert("RGB").resize(self.newDate, Image.BICUBIC)
        return pic

    def getFullScale(self):
        "Iškerpa skalę"
        scale = self.pic.crop(self.scale)
        scale = scale.rotate(90)
        return scale

    def compose(self):
        "Sudeda žemėlapį ir datą"
        map = self.getMap()
        date = self.getDate()

        canvas = Image.new("RGB", self.canvasSize, (0, 0, 0))
        canvas.paste(date, self.dateOffset)
        canvas.paste(map,  self.mapOffset)
        return canvas

    def empty(self):
        "Nupaišom baltą tuščią paveiksliuką"
        return Image.new("RGB", self.canvasSize, (255, 255, 255))

class PrecipitationPicture(WindPicture):
    """Kritulių paveiksliuko gavimas/aprodojimas"""

    url = "http://www.wetterzentrale.de/pics/Rtavn%s4.gif"
    maskName = "crop-map-small.png"
    map =   rect(500, 217, 140, 139)
    mapoffset = (1, -1)
    date =  rect(536, 5, 257, 16)
    newDate = (142, 8)
    scale = rect(810, 160, 30, 330)
    canvasSize = (142, 149)
    dateOffset = (0, 0)
    mapOffset = (1, 9)


class TempPicture(PrecipitationPicture):
    """Temperatūros paveiksliuko gavimas/apdorojimas"""


    url = "http://www.wetterzentrale.de/pics/Rtavn%s5.gif"
    scale = rect(806, 130, 44, 425)

hours = ["%02d" % i for i in range(0, 164, 6)]

def generate():
    """Susiurbia ir iškarpo visus paveiksliukus"""

    for hr in hours:
        pic = WindPicture(hr)
        pic.compose().save(os.path.join(outputdir, "Rtavn%s9.png" % hr))
        if hr == '00':
            pic.getFullScale().save(os.path.join(outputdir, "scale.png"))

    for hr in hours:
        pic = TempPicture(hr)
        pic.compose().save(os.path.join(outputdir, "Rtavn%s5.png" % hr))
        if hr == '00':
            pic.getFullScale().save(os.path.join(outputdir, "tscale.png"))

    for hr in hours:
        if hr == '00':
            continue
        pic = PrecipitationPicture(hr)
        pic.compose().save(os.path.join(outputdir, "Rtavn%s4.png" % hr))
        if hr == '06':
            pic.getFullScale().save(os.path.join(outputdir, "pscale.png"))
            # Miuleris neduoda 00, pakeičiam tuščiu
            pic.empty().save(os.path.join(outputdir, "Rtavn004.png"))


def tstamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def makeIndex(filename, **kw):
    """Vėjo, temperatūros ir kritulių indeksai"""
    template = PageTemplateFile(os.path.join(dirname, 'pt', 'index.pt'))
    index = open(os.path.join(outputdir, filename), "w")
    kw['hours'] = hours
    kw['time'] = tstamp()
    if 'extra' not in kw:
        kw['extra'] = ''
    index.write(template(kw).encode('utf-8'))
    index.close()


def tableIndex(extra='', **kw):
    """Padaro HTML indeksą su visos savaitės visais paveiksliukais
    lentelėje"""
    template = PageTemplateFile(os.path.join(dirname, 'pt', 'tabindex.pt'))
    index = open(os.path.join(outputdir, 'viskas.html'), "w")
    kw['hours'] = hours
    kw['title'] = u'Vėjas, temperatūra, krituliai'
    kw['time'] = tstamp()
    index.write(template(kw).encode('utf-8'))
    index.close()

def hourIndexes():
    """Kiekvienos valandos indeksai su 3 žemėlapiais"""
    template = PageTemplateFile(os.path.join(dirname, 'pt', 'hour.pt'))
    cur = prev = None
    for next in hours + [None]:
        if cur is not None:
            index = open(os.path.join(outputdir, "%s.html" % cur), "w")
            result = template({'title': '+%s h' % cur,
                               'prev': prev, 'cur': cur,
                               'next': next,
                               'time': tstamp()})
            index.write(result.encode('utf-8'))
            index.close()
        prev = cur
        cur = next

def mobileIndex(extra='', **kw):
    """Padaro HTML indeksą su visos savaitės visais paveiksliukais
    lentelėje"""
    template = PageTemplateFile(os.path.join(dirname, 'pt', 'mobile.pt'))
    index = open(os.path.join(outputdir, 'delninis.html'), "w")
    kw['hours'] = hours
    kw['title'] = u'Vėjas, temperatūra, krituliai'
    kw['time'] = tstamp()
    index.write(template(kw).encode('utf-8'))
    index.close()

    for name in ('back2dm', 'aukst2dm', 'didz2dm', 'svent2dm', 'vili2dm',
                 'silute2dm', 'klp2dm'):
        file = open( name + '.html', "w")
        file.write('''<html>
        <head><title>%(name)s</title></head>
        <body>
        <a href="delninis.html">Atgal</a><br>
        <img src="%(name)s.png" alt="%(name)s">
        </body></html>
        ''' % {'name': name})
        file.close()

def istorijaIndex():
    """Padaro HTML su KOSIS RRD grafikais."""

    template = PageTemplateFile(os.path.join(dirname, 'pt', 'istorija.pt'))
    index = open(os.path.join(outputdir, "istorija.html"), "w")
    result = template({'stoteles': ['aukst', 'viev', 'back', 'viln',
                                    'svent', 'silute', 'klp'],
                       'title': 'KOSIS istorija'})
    index.write(result.encode('utf-8'))
    index.close()

def main(args):
    if len(args) > 1:
        global outputdir
        outputdir = sys.argv[1]

    extra=""
    if os.path.exists(os.path.join(outputdir, "aukst2d.png")):
        extra = '''<p><img src="aukst2d.png"
                           alt="KOSIS istorija"
                           title="KOSIS istorija"></p>'''

    makeIndex(filename="index.html", picfmt="Rtavn%s9.png",
              title=u"Vėjas", scale="scale.png", extra=extra)
    makeIndex(filename="temp.html", picfmt="Rtavn%s5.png",
              title=u"Temperatūra", scale="tscale.png")
    makeIndex(filename="precipitation.html", picfmt="Rtavn%s4.png",
              title="Krituliai", scale="pscale.png")
    hourIndexes()
    tableIndex(extra=extra)
    mobileIndex()
    istorijaIndex()
    if '-n' not in args:
        generate()

if __name__ == '__main__':
    main(sys.argv)

