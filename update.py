#!/usr/bin/python
# -*- coding: utf-8 -*-
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

from datetime import datetime
import sys
from os import system, popen
import os.path

from eismoinfo import EismoInfo


outputdir = "."


def update(db, tstamp, value):
    """Update RRD database db with value at a given time.

    An update is only performed if the time is more than the last
    update time.
    """

    db = os.path.join(outputdir, db)

    cmdline = "rrdtool update -s %s %i:%f" % (db, tstamp, value)
    system(cmdline)


def vg_text(einfo):
    readouts = [(r.timestamp, r) for r in einfo.get(u'Aukštadvaris', [])]
    if not readouts:
        return
    readouts.sort()
    d = readouts[-1][1]

    out = file(os.path.join(outputdir, "vgmeteo.html"), "w")

    e = lambda s: s.encode("windows-1257")
    print >> out, e(u"<h3>%s</h3>" % d.name)
    print >> out, e(u"<p>%s</p>" % datetime.fromtimestamp(d.timestamp))
    print >> out, e(u"<img src='aukstvg.png' alt=''>")
    print >> out, e(u"<table>")
    print >> out, e(u" <tr><th>Vid. vėjo greitis</th><td>%.0f m/s</td></tr>"
                    % d.avg)
    print >> out, e(u" <tr><th>Vėjo kryptis</th><td>%s</td></tr>" % d.dir_txt)
    print >> out, e(u" <tr><th>Oro temperatūra</th><td>%s&deg;C</td></tr>" % d.temp)
    print >> out, e(u" <tr><th>Rasos taškas</th><td>%s&deg;C</td></tr>" % d.dew)
    print >> out, e(u" <tr><th>Kritulių tipas</th><td>%s</td></tr>"
                   % d.precipitation_type)
    print >> out, e(u" <tr><th>Kritulių kiekis</th><td>%s mm</td></tr>"
                   % d.precipitation)
    print >> out, e(u"</table>")


def main(args):

    if len(sys.argv) > 1:
        global outputdir
        outputdir = sys.argv[1]

    einfo = EismoInfo()

    for name, prefix in [
        (u'Aukštadvaris', 'aukst'),
        (u'Bačkonys', 'back'),
        (u'Vilnius', 'viln'),
        (u'Vievis', 'viev'),
        (u'Šventoji', 'svent'),
        (u'Šilutė', 'silute'),
        (u'Klaipėda', 'klp')]:
        try:
            for readout in einfo[name]:
                update("%s-max.rrd" % prefix, readout.timestamp, readout.max)
                update("%s-avg.rrd" % prefix, readout.timestamp, readout.avg)
                update("%s-dir.rrd" % prefix, readout.timestamp, readout.dir)
        except KeyError:
            pass

    system("sh graph.sh %s > /dev/null 2>&1 " % outputdir)

    vg_text(einfo)


if __name__ == '__main__':
    main(sys.argv)
