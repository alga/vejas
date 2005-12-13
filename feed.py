#!/usr/bin/env python
'''
  KOSIS duomenø ðienavimas Vëjo Galvoje projektui.

  2003 Albertas Agejevas.

  $Id: feed.py,v 1.2 2003/05/29 22:52:32 alga Exp $
'''

from kosis import KOSIS
from traceback import print_exc
import urllib


stoteles = (
    ('Salociai', 'S', 'http://www.lra.lt/auto/kosis/id510.html'),
    ('Sventoji', 'V', 'http://www.lra.lt/auto/kosis/id810.html'),
    ('Kalvarija', 'P', 'http://www.lra.lt/auto/kosis/id330.html'),
    ('Pirciupiai', 'P', 'http://www.lra.lt/auto/kosis/id20.html'),
    ('Zarasai', 'R', 'http://www.lra.lt/auto/kosis/id920.html'),
    ('Vilijampole', 'C', 'http://www.lra.lt/auto/kosis/id430.html'),
    ('Backonys', 'R', 'http://www.lra.lt/auto/kosis/id110.html'),
    ('Ausktadvaris', 'R', 'http://www.lra.lt/auto/kosis/id1110.html'),
    ('Didziulio ez.', 'R', 'http://www.lra.lt/auto/kosis/id100.html'),
    ('Seirijai', 'P', 'http://www.lra.lt/auto/kosis/id10.html')
    )

def upload(regionas, vieta, kosis):
    url = 'http://www.vejasgalvoje.lt/ws/orai.cgi'

    kw = ('source', 'region', 'location', 'laikas', 'temperatura',
          'krituliai', 'vejas', 'kryptis')

    url += ('?source=K&'
            'region=%s&'
            'location=%s&'
            'laikas=%s&'
            'temperatura=%s&'
            'krituliai=%s&'
            'vejas=%3.1f-%d&'
            'kryptis=%s' % (regionas, vieta,
                            kosis.dt.strftime("%Y-%m-%d%%20%H:%M:%S"),
                            kosis.temp, '%3f',
                            kosis.avg, int(kosis.max+0.5), kosis.kryptis))

    handle = urllib.urlopen(url)
    handle.read()
    handle.close()

if __name__ == '__main__':

    for stotis in stoteles:
        duom = KOSIS(stotis[2])
        ## print "%20s %s vëjas %s m/s, max %s m/s, %s °C" % \
        ##       (stotis[0], stotis[1], duom.avg, duom.max, duom.temp)
        if duom.avg is not None:
            upload(stotis[1], stotis[0], duom)
