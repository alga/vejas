#!/usr/bin/python
# -*- coding: iso-8859-13 -*-
'''
     Informacijos iš KOSIS sudėjimas į RRD
     Copyright (C) 2002 Albertas Agejevas

     This program is free software; you can redistribute it and/or
     modify it under the terms of the GNU General Public License
     as published by the Free Software Foundation; either version 2
     of the License, or (at your option) any later version.

     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     $Id: update.py,v 1.7 2005/07/19 10:40:28 alga Exp $
'''
import datetime
import urllib
import cElementTree
from pprint import pprint


class KOSIS(object):
    url = "http://www.lra.lt/maps/getxml.php?xml=weather_lt"

    def __init__(self):
        doc = urllib.urlopen(self.url).read()
        tree = cElementTree.fromstring(doc)

        self.data = {}
        for item in tree.findall("weather/item"):
            readout = Readout(item)
            if readout.timestamp:
                if readout.name not in self.data:
                    self.data[readout.name] = []
                self.data[readout.name].append(readout)


class Readout(object):
    """An object that represents a single readout from a weather station"""

    deg = {u'Š': 0,   u'ŠR': 45, u'R': 90, u'PR': 135,
           u'P': 180, u'PV': 225, u'V': 270, u'ŠV': 315, u'-': 0}

    def __init__(self, node):
        self.name = node.find('name').text
        self.timestamp = self.parsetime(node.find('time').text)
        self.max = float(node.find('wind_speed_max').text)
        self.avg = float(node.find('wind_speed_avg').text)
        self.dir_txt = node.find('wind_direction').text
        self.dir = self.deg[self.dir_txt]
        self.precipitation = float(node.find('krit_kiekis').text)
        self.precipitation_type = node.find('krit_tipas').text
        self.temp = float(node.find('air_temp').text.replace(",", "."))
        self.dew = float(node.find('rasos_temp').text.replace(",", "."))

    def parsetime(self, datetimestr):
        try:
            datestr, timestr = datetimestr.split()
            month, day = map(int, datestr.split('-'))
            hour, minute = map(int, timestr.split(":"))
        except (ValueError, TypeError):
            return None
        timestamp = datetime.datetime.now()
        timestamp = timestamp.replace(month=month, day=day,
                                      hour=hour, minute=minute,
                                      second=0, microsecond=0)
        return guess_year(timestamp)

    def __repr__(self):
        return "Readout(%r, %s, %r, %r, %r)" % (self.name, self.timestamp,
                                                self.avg, self.max, self.dir)


def guess_year(dt):
    """Chooses the year of the datetime to be closest to current moment"""
    choices = []
    now = datetime.datetime.now()
    choices.append((abs(dt - now), dt))
    try:
        dt1 = dt.replace(year=dt.year - 1)
        choices.append((abs(dt1 - now), dt1))
    except ValueError:
        pass
    try:
        dt2 = dt.replace(year=dt.year + 1)
        choices.append((abs(dt2 - now), dt2))
    except ValueError:
        pass
    choices.sort()
    return choices[0][1]


if __name__ == '__main__':

    k = KOSIS()
    for st in k.data:
        for datum in k.data[st]:
            print repr(datum)
