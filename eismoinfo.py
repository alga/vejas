#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Informacijos iš eismoinfo.lt sudėjimas į RRD

Copyright (C) 2012-2018 Albertas Agejevas

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
import json
import requests
import pprint


class EismoInfo(dict):

    url = 'http://eismoinfo.lt/weather-conditions-service'

    ids = {
        'aukst': 1163,
        'back': 1208,
        'viln': 1166,
        'viev': 308,
        'svent': 981,
        'silute': 984,
        'klp': 1187,
        }

    def __init__(self):
        super(EismoInfo, self).__init__()
        response = requests.get(self.url)
        # WTF, some trailing junk after JSON
        data = json.loads(response.text.split('<!DOCTYPE')[0])
        readouts = {}
        for readout in data:
            readouts[int(readout['id'])] = readout
        self.data = {}
        for station_id in self.ids.values():
            station = Station(readouts[station_id])
            self[station.name] = [station]


class Station(object):

    # [{"surinkimo_data_unix":"1524339300",
    #   "surinkimo_data":"2018-04-21 22:35:00",
    #   "id":"1166",
    #   "irenginys":"Vilnius",
    #   "numeris":"A1",
    #   "pavadinimas":"Vilnius\u2013Kaunas\u2013Klaip\u0117da",
    #   "kilometras":"10.04",
    #   "oro_temperatura":"9.6",
    #   "vejo_greitis_vidut":"0.4",
    #   "krituliu_tipas":"N\u0117ra",
    #   "krituliu_kiekis":"0",
    #   "dangos_temperatura":"14",
    #   "matomumas":"2000",
    #   "rasos_taskas":"1.74",
    #   "kelio_danga":"Sausa",
    #   "uzsalimo_taskas":null,
    #   "vejo_greitis_maks":"1.4",
    #   "vejo_kryptis":"Pietry\u010di\u0173",
    #   "sukibimo_koeficientas":"0.82",
    #   "ilguma":"576155","platuma":"6056858",
    #   "lat":"54.642475","lng":"25.17984"}, ...]

    deg = {u'Šiaurės': 0,   u'Šiaurės rytų': 45, u'Rytų': 90,
           u'Pietryčių': 135, u'Pietų': 180, u'Pietvakarių': 225,
           u'Vakarų': 270, u'Šiaurės vakarų': 315}

    def __init__(self, data):
        try:
            self.name = data["irenginys"]
            self.timestamp = int(data["surinkimo_data_unix"])
            self.avg = float(data["vejo_greitis_vidut"] or 0)
            self.max = float(data["vejo_greitis_maks"] or 0)
            self.dir_txt = data["vejo_kryptis"]
            self.dir = self.deg.get(self.dir_txt, 0)
            self.temp = float(data["oro_temperatura"] or 0)
            self.dew = float(data["rasos_taskas"] or 0)
            self.precipitation_type = data["krituliu_tipas"]
            self.precipitation = float(data["krituliu_kiekis"] or 0)
        except Exception:
            pprint.pprint(data)
            raise
