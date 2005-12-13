#!/usr/bin/env python
"""
  muller.py

  Process wind forecasts by Georg Müller (http://www.wetterzentrale.de/)

$Id: muller.py,v 1.10 2003/05/23 13:19:02 alga Exp $
"""

from PIL import Image
from muller import WindPicture

class WapWindPicture(WindPicture):
    pass


img = Image.open("Rtavn009.png")
img = img.crop((35, 54, 35+95, 54+75))

for x in range(95):
    for y in range(75):
        if img.getPixel((x,y)) == 0:
            pass
