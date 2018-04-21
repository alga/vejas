#!/bin/sh
# Create databases for wind stats
# $Id: create.sh,v 1.8 2005/07/19 10:40:28 alga Exp $

start=`date +%s -d "2 weeks ago"`

for db in aukst back viln viev svent silute klp; do
    rrdtool create -b $start $db-max.rrd DS:max:GAUGE:9600:0:30  RRA:MAX:0.5:1:4000
    rrdtool create -b $start $db-avg.rrd DS:avg:GAUGE:9600:0:30  RRA:AVERAGE:0.5:1:4000
    rrdtool create -b $start $db-dir.rrd DS:dir:GAUGE:9600:0:360 RRA:AVERAGE:0.5:1:4000
done
