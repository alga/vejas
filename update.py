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

    for dt, max, avg, dir in kosis.data[u'Aukštadvaris']:
        update("aukst-max.rrd", dt, max)
        update("aukst-avg.rrd", dt, avg)
        update("aukst-dir.rrd", dt, dir)

    for dt, max, avg, dir in kosis.data[u'Bačkonys']:
        update("back-max.rrd", dt, max)
        update("back-avg.rrd", dt, avg)
        update("back-dir.rrd", dt, dir)

    for dt, max, avg, dir in kosis.data[u'Didžiulio ež.']:
        update("didz-max.rrd", dt, max)
        update("didz-avg.rrd", dt, avg)
        update("didz-dir.rrd", dt, dir)

    for dt, max, avg, dir in kosis.data[u'Šventoji']:
        update("svent-max.rrd", dt, max)
        update("svent-avg.rrd", dt, avg)
        update("svent-dir.rrd", dt, dir)

    for dt, max, avg, dir in kosis.data[u'Vilijampolė']:
        update("vili-max.rrd", dt, max)
        update("vili-avg.rrd", dt, avg)
        update("vili-dir.rrd", dt, dir)

    for dt, max, avg, dir in kosis.data[u'Šilutė']:
        update("silute-max.rrd", dt, max)
        update("silute-avg.rrd", dt, avg)
        update("silute-dir.rrd", dt, dir)

    for dt, max, avg, dir in kosis.data[u'Klaipėda']:
        update("klp-max.rrd", dt, max)
        update("klp-avg.rrd", dt, avg)
        update("klp-dir.rrd", dt, dir)

    system("sh graph.sh > /dev/null 2>&1")

