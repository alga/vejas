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

import time
from os import system, popen

from kosisxml import KOSIS

def update(db, tstamp, value):
    """Update RRD database db with value at a given time.

    An update is only performed if the time is more than the last
    update time.
    """

    timestamp = time.mktime(tstamp.timetuple())
    last = int(popen("rrdtool last %s" % db).read())

    if last < timestamp:
        cmdline = "rrdtool update %s %i:%f" % (db, timestamp, value)
        system(cmdline)


if __name__ == '__main__':

    kosis = KOSIS()

    for name, prefix in [
        (u'Aukštadvaris', 'aukst'),
        (u'Bačkonys', 'back'),
        (u'Didžiulio ež.', 'didz'),
        (u'Šventoji', 'svent'),
        (u'Vilijampolė', 'vili'),
        (u'Šilutė', 'silute'),
        (u'Klaipėda', 'klp')]:
        try:
            for dt, max, avg, dir in kosis.data[name]:
                update("%s-max.rrd" % prefix, dt, max)
                update("%s-avg.rrd" % prefix, dt, avg)
                update("%s-dir.rrd" % prefix, dt, dir)
        except KeyError:
            pass

    system("sh graph.sh > /dev/null 2>&1")

