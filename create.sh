#!/bin/sh
# Create databases for wind stats
# $Id: create.sh,v 1.8 2005/07/19 10:40:28 alga Exp $

rrdtool create aukst-max.rrd DS:max:GAUGE:9600:0:30  RRA:MAX:0.5:1:4000
rrdtool create aukst-avg.rrd DS:avg:GAUGE:9600:0:30  RRA:AVERAGE:0.5:1:4000
rrdtool create aukst-dir.rrd DS:dir:GAUGE:9600:0:360 RRA:AVERAGE:0.5:1:4000

rrdtool create back-max.rrd DS:max:GAUGE:9000:0:30  RRA:MAX:0.5:1:4000
rrdtool create back-avg.rrd DS:avg:GAUGE:9000:0:30  RRA:AVERAGE:0.5:1:4000
rrdtool create back-dir.rrd DS:dir:GAUGE:9000:0:360 RRA:AVERAGE:0.5:1:4000

rrdtool create didz-max.rrd DS:max:GAUGE:9000:0:30  RRA:MAX:0.5:1:4000
rrdtool create didz-avg.rrd DS:avg:GAUGE:9000:0:30  RRA:AVERAGE:0.5:1:4000
rrdtool create didz-dir.rrd DS:dir:GAUGE:9000:0:360 RRA:AVERAGE:0.5:1:4000

rrdtool create svent-max.rrd DS:max:GAUGE:9000:0:30  RRA:MAX:0.5:1:4000
rrdtool create svent-avg.rrd DS:avg:GAUGE:9000:0:30  RRA:AVERAGE:0.5:1:4000
rrdtool create svent-dir.rrd DS:dir:GAUGE:9000:0:360 RRA:AVERAGE:0.5:1:4000

rrdtool create vili-max.rrd DS:max:GAUGE:9000:0:30  RRA:MAX:0.5:1:4000
rrdtool create vili-avg.rrd DS:avg:GAUGE:9000:0:30  RRA:AVERAGE:0.5:1:4000
rrdtool create vili-dir.rrd DS:dir:GAUGE:9000:0:360 RRA:AVERAGE:0.5:1:4000

rrdtool create silute-max.rrd DS:max:GAUGE:9000:0:30  RRA:MAX:0.5:1:4000
rrdtool create silute-avg.rrd DS:avg:GAUGE:9000:0:30  RRA:AVERAGE:0.5:1:4000
rrdtool create silute-dir.rrd DS:dir:GAUGE:9000:0:360 RRA:AVERAGE:0.5:1:4000

rrdtool create klp-max.rrd DS:max:GAUGE:9000:0:30  RRA:MAX:0.5:1:4000
rrdtool create klp-avg.rrd DS:avg:GAUGE:9000:0:30  RRA:AVERAGE:0.5:1:4000
rrdtool create klp-dir.rrd DS:dir:GAUGE:9000:0:360 RRA:AVERAGE:0.5:1:4000

