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

    deg = {u'Š': 0,   u'ŠR': 45, u'R': 90, u'PR': 135,
           u'P': 180, u'PV': 225, u'V': 270, u'ŠV': 315, u'-': 0}

    def __init__(self):
        doc = urllib.urlopen(self.url).read()
        tree = cElementTree.fromstring(doc)

        self.data = {}
        for item in tree.findall("weather/item"):
            timestamp = datetime.datetime.now()
            try:
                datestr, timestr = item.find('time').text.split()
                month, day = map(int, datestr.split('-'))
                hour, minute = map(int, timestr.split(":"))
            except (ValueError, TypeError):
                pass
            else:
                timestamp = timestamp.replace(month=month, day=day,
                                              hour=hour, minute=minute,
                                              second=0, microsecond=0)

                name = item.find('name').text
                max = float(item.find('wind_speed_max').text)
                avg = float(item.find('wind_speed_avg').text)
                dir_txt = item.find('wind_direction').text
                dird = self.deg[dir_txt]
                if name not in self.data:
                    self.data[name] = []
                self.data[name].append((timestamp, max, avg, dird))

if __name__ == '__main__':

    k = KOSIS()
    for st in k.data:
        for dt, max, avg, dir in k.data[st]:
            print dt, max, avg, dir, st
