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
import sys
import json
import requests

import eismoinfo
from update import update


URL = "http://eismoinfo.lt/weather-conditions-retrospective?id={0}&number={1}"

def main():
    for station, code in eismoinfo.EismoInfo.ids.items():
        print
        print station
        text = requests.get(URL.format(code, 1000)).text
        data = json.loads(text.split('<!DOCTYPE')[0])
        data.sort(key=lambda d: d["surinkimo_data_unix"])
        for i, item in enumerate(data):
            if i % 50 == 0:
                sys.stdout.write(".")
                sys.stdout.flush()
            item["irenginys"] = station
            readout = eismoinfo.Station(item)
            # TODO: bunch up updates into a single command
            update("%s-max.rrd" % station, readout.timestamp, readout.max)
            update("%s-avg.rrd" % station, readout.timestamp, readout.avg)
            update("%s-dir.rrd" % station, readout.timestamp, readout.dir)
    print


if __name__ == "__main__":
    main()
