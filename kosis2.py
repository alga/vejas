#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
     Informacijos iš eismoinfo.lt sudėjimas į RRD
     Copyright (C) 2012 Albertas Agejevas

     This program is free software; you can redistribute it and/or
     modify it under the terms of the GNU General Public License
     as published by the Free Software Foundation; either version 2
     of the License, or (at your option) any later version.

     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.
'''
import datetime
import os
from BeautifulSoup import BeautifulSoup
from pprint import pprint


class KOSIS(object):

    url = ("http://www.eismoinfo.lt/lt/traffic-map?"
           "q=lt/traffic-map-info-window&type=device&id=%d")

    ids = {
        'aukst': 1163,
        'back': 107,
        'viln': 1166,
        'viev': 308,
        'svent': 981,
        'silute': 984,
        'klp': 111,
        }

    def __init__(self):
        self.data = {}
        for id_ in self.ids.values():
	    try:
            	station = Station(self.url % id_)
            except Exception, e:
                # print "Error for %s: %s" % (id_, e)
		pass
            else:
                self.data[station.name] = [station]


class Station(object):

    deg = {u'Šiaurės': 0,   u'Šiaurės rytų': 45, u'Rytų': 90,
           u'Pietryčių': 135, u'Pietų': 180, u'Pietvakarių': 225,
           u'Vakarų': 270, u'Šiaurės vakarų': 315}

    def __init__(self, url):
        self.url = url
        #doc = urllib.urlopen(self.url).read()
        # Server replies 'HTTP/1.1 Ok 200 \r\n', which breaks urllib?
        doc = os.popen("curl '%s' 2> /dev/null" % self.url).read()
        soup = BeautifulSoup(doc)
        title = soup.find('div', {'class': 'title'})
        self.name = title.text if title else ''

        data = dict([[e.text for e in row.findAll('td')]
                     for row in soup.findAll('tr')])

        # [u'Surinkimo data:', u'2012-04-08 14:50']
        # [u'Krituli\u0173 intensyvumas (mm/h):', u'0']
        # [u'Krituli\u0173 tipas:', u'N\u0117ra']
        # [u'Matomumas (m):', u'640']
        # [u'Oro temperat\u016bra (&#8451;):', u'-0,3']
        # [u'Rasos ta\u0161kas (&#8451;):', u'-1,4']
        # [u'Kelio dangos b\u016bkl\u0117:', u'\u0160lapia']
        # [u'Kelio dangos temperat\u016bra (&#8451;):', u'2,7']
        # [u'U\u017e\u0161\u0105limo ta\u0161kas (&#8451;):', u'']
        # [u'Vidut. v\u0117jo greitis (m/s):', u'4,7']
        # [u'V\u0117jo kryptis:', u'Vakar\u0173']

        def fl(key):
            if data[key]:
                return float(data[key].replace(",", "."))
            else:
                return 0.0

        self.timestamp = datetime.datetime.strptime(
            data[u'Surinkimo data:'], "%Y-%m-%d %H:%M")
        self.avg = fl(u'Vidut. v\u0117jo greitis (m/s):')
        self.max = fl(u'Maks. v\u0117jo greitis (m/s):')
        self.dir_txt = data[u'V\u0117jo kryptis:']
        self.dir = self.deg.get(self.dir_txt, 0)
        self.precipitation = fl(u'Krituli\u0173 intensyvumas (mm/h):')
        self.precipitation_type = data[u'Krituli\u0173 tipas:']
        self.temp = fl(u'Oro temperat\u016bra (&#8451;):')
        self.dew = fl(u'Rasos ta\u0161kas (&#8451;):')

