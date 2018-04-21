#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Informacijos iš EismoInfo.lt sudėjimas į RRD.

Copyright (C) 2018 Albertas Agejevas

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
import os
import sys
import json
import requests

import eismoinfo
import update


from itertools import izip_longest as zip_longest # for Python 2.x
#from itertools import zip_longest # for Python 3.x
#from six.moves import zip_longest # for both (uses the six compat library)
# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks/312464
def grouper(n, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)


URL = "http://eismoinfo.lt/weather-conditions-retrospective?id={0}&number={1}"

outputdir = "."

def main():
    if len(sys.argv) > 1:
        global outputdir
        update.outputdir = outputdir = sys.argv[1]

    for station, code in eismoinfo.EismoInfo.ids.items():
        print station
        text = requests.get(URL.format(code, 1500)).text
        data = json.loads(text.split('<!DOCTYPE')[0])
        data.sort(key=lambda d: d["surinkimo_data_unix"])
        for chunk in grouper(100, data):
            sys.stdout.write(".")
            sys.stdout.flush()
            maxes = []
            avgs = []
            dirs = []
            for item in chunk:
                if item is None:
                    break
                item["irenginys"] = station
                readout = eismoinfo.Station(item)
                maxes.append((readout.timestamp, readout.max))
                avgs.append((readout.timestamp, readout.avg))
                dirs.append((readout.timestamp, readout.dir))
            # TODO: bunch up updates into a single command
            update.update("%s-max.rrd" % station, maxes)
            update.update("%s-avg.rrd" % station, avgs)
            update.update("%s-dir.rrd" % station, dirs)
        print

    os.system("sh graph.sh %s > /dev/null 2>&1 " % outputdir)


if __name__ == "__main__":
    main()
