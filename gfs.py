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
import re
import os.path
from PIL import Image, ImageDraw
from cStringIO import StringIO
from zope.pagetemplate.pagetemplatefile import PageTemplateFile

dirname = os.path.dirname(__file__)
outputdir = "."


def rect(x, y, w, h):
    return (x, y, x + w, y + h)


class WindPicture:
    """Vėjo paveiksliuko gavimas/apdorojimas"""

    url = "http://www.wetterzentrale.de/pics/Rtavn%s9.png"
    maskName = os.path.join(dirname, "crop-map.png")
    map =   rect(474, 56, 214, 158)
    mapoffset = (20, 0)
    date =  rect(476, 0, 257, 16)
    scale = rect(740, 65, 35, 489)
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
        self.hr = hr
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

    url = "http://www.wetterzentrale.de/pics/Rtavn%s4.png"
    maskName = "crop-map-small.png"
    map =   rect(449, 217, 140, 139)
    mapoffset = (1, -1)
    date =  rect(476, 0, 257, 16)
    newDate = (142, 8)
    scale = rect(750, 160, 30, 330)
    canvasSize = (142, 149)
    dateOffset = (0, 0)
    mapOffset = (1, 9)


class TempPicture(PrecipitationPicture):
    """Temperatūros paveiksliuko gavimas/apdorojimas"""

    url = "http://www.wetterzentrale.de/pics/Rtavn%s5.png"
    scale = rect(748, 110, 44, 425)


class WavePicture(WindPicture):
    """Lenkiškas bangavimo paveiksliukas"""

    t0 = None
    url = None
    url_format = "http://falowanie.icm.edu.pl/pict/wavehgt%%s.%s.GIF"
    scale_url = "http://falowanie.icm.edu.pl/pictconst/wavehgt.legend.gif"
    index_url = "http://falowanie.icm.edu.pl/english/wavefrcst.html"

    date_re = "<B>start \(t<sub>0</sub>\) : (.*)</B>"
    url_re = "\.([0-9]{5})\.GIF"
    map = rect(100, 398, 300, 248)
    outsize = (150, 124)
    textpos = (2, 114)

    def __init__(self, hr=None, file=None):
        if self.url is None:
            self.text = urllib.urlopen(self.index_url).read()

            numbers = re.search(self.url_re, self.text).group(1)
            WavePicture.url = self.url_format % numbers
            WavePicture.t0 = self.getT0()
        WindPicture.__init__(self, hr, file)

    def getT0(self):
        match = re.search(self.date_re, self.text)
        datestr = match.group(1)
        dtuple = time.strptime(datestr, "%A, %d %B %y, %H:%M UTC")
        return datetime.datetime(*dtuple[:6])

    def compose(self):
        im =  self.getMap().resize(self.outsize, Image.BICUBIC)
        draw = ImageDraw.Draw(im)
        x, y = self.textpos
        draw.rectangle((x, y+1, x+136, y+12), fill="white")
        draw.text(self.textpos, "%s UTC" % self.date, fill="black")
        del draw
        return im

    def getFullScale(self):
        data = urllib.urlopen(self.scale_url)
        file = StringIO(data.read())
        pic = Image.open(file).convert("RGB")
        return pic.resize((55, 300), Image.BICUBIC).rotate(90)

    @property
    def date(self):
        return self.t0 + datetime.timedelta(hours=int(self.hr))


class ICMWindPicture(WavePicture):

    url_format = "http://meteo.icm.edu.pl/pict/forecast18/wind10m_pl%%s.%s.GIF"
    index_url = "http://meteo.icm.edu.pl/"
    url_re = 'var KON="([0-9]{5})"'

    map = rect(426, 0, 301, 240)
    outsize = (150, 120)
    textpos = (2, 110)
    scale = rect(730, 155, 120, 600)
    scalesize = (300, 60)

    def getT0(self):
        y = int(re.search("var Year=([0-9]+)", self.text).group(1))
        m = int(re.search("var Month=([0-9]+)", self.text).group(1))
        d = int(re.search("var Day=([0-9]+)", self.text).group(1))
        h = int(re.search("var Start_time=([0-9]+)", self.text).group(1))
        return datetime.datetime(y, m, d, h)

    def getFullScale(self):
        "Iškerpa skalę"
        scale = self.pic.crop(self.scale)
        scale = scale.rotate(270).convert("RGB")
        return scale.resize(self.scalesize, Image.BICUBIC)


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

    for hr in hours[1:9]:
        pic = WavePicture(hr)
        pic.compose().save(os.path.join(outputdir, "wavehgt%s.png" % hr))

    pic.getFullScale().save(os.path.join(outputdir, "wscale.png"))

    WavePicture.t0 = WavePicture.url = None

    for hr in hours[1:9]:
        pic = ICMWindPicture(hr)
        pic.compose().save(os.path.join(outputdir, "lenkai%s.png" % hr))

    pic.getFullScale().save(os.path.join(outputdir, "lenkai_scale.png"))


def tstamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def makeIndex(filename, **kw):
    """Vėjo, temperatūros ir kritulių indeksai"""
    pt = kw.get('template', 'index.pt')
    template = PageTemplateFile(os.path.join(dirname, 'pt', pt))
    index = open(os.path.join(outputdir, filename), "w")
    if 'hours' not in kw:
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
    result = template({'stoteles': ['aukst', 'back', 'didz', 'vili',
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
    makeIndex(filename="waves.html", picfmt="wavehgt%s.png",
              title="Bangos", scale="wscale.png", hours=hours[1:9],
              template="waves.pt")
    makeIndex(filename="lenkai.html", picfmt="lenkai%s.png",
              title="Lenkai", scale="lenkai_scale.png", hours=hours[1:9],
              template="waves.pt")
    hourIndexes()
    tableIndex(extra=extra)
    mobileIndex()
    istorijaIndex()
    if '-n' not in args:
        generate()


if __name__ == '__main__':
    main(sys.argv)

