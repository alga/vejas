#!/usr/bin/python
# -*- coding: iso-8859-13 -*-
'''
     Informacijos ištraukimas iš KOSIS
     Copyright (C) 2002 Albertas Agejevas

     This program is free software; you can redistribute it and/or
     modify it under the terms of the GNU General Public License
     as published by the Free Software Foundation; either version 2
     of the License, or (at your option) any later version.

     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     $Id: kosis.py,v 1.9 2005/01/26 14:15:13 alga Exp $
'''

import urllib
from mx.DateTime.mxDateTime import DateTime

deg = {
    'S': 0,   'SR': 45, 'R': 90, 'PR': 135,
    'P': 180, 'PV': 225, 'V': 270, 'SV': 315,
    }

class KOSIS:
    dict = {}
    def __init__(self, url='http://www.lra.lt/auto/kosis/id1110.html'):
        self.url = url
        self.parse()

    def parse(self):
        data = self.data = {}
        try:
            page = urllib.urlopen(self.url)
            for line in page.readlines():
                if line.find(' : ') != -1:
                    line = line.split(':', 1)
                    key = line[0].strip()
                    value = line[1].strip()
                    data[key] = value
        except IOError:
            pass

        try:
            v = data['VÄjo kryptis'].replace('Å ','S')
            self.dir = deg[v]
            self.kryptis = v
        except KeyError:
            self.dir = None
            self.kryptis = '?'

        try:
            avg = data['Vidutinis vÄjo greitis']
            self.avg = float(avg.split()[0].replace(',','.'))
        except KeyError:
            self.avg = None

        try:
            max = data['Maksimalus vÄjo greitis']
            self.max = float(max.split()[0].replace(',','.'))
        except KeyError:
            self.max = None

        try:
            temp = data['Oro temperatÅ«ra'].replace("Ā°", "°")
            self.temp = float(temp.split('°')[0].replace(',','.'))
        except KeyError:
            self.temp = None

        try:
            date = data['Paskutinis nuskaitymas']
            d, t = date.split()
            y, m, d = map(int, d.split("-"))
            h, min = map(int, t.split(":"))
            self.dt = DateTime(y, m, d, h, min)
            self.time = int(self.dt.strftime('%s'))
        except KeyError:
            self.dt = self.time = None

    def __str__(self):
        return "avg %.1f max %.1f dir %d temp %.1f time %d" % \
               (self.avg, self.max, self.dir, self.temp, self.time, )

if __name__ == '__main__':
    print KOSIS()

