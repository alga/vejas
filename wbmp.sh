#!/bin/sh

OUT=${1:-.}

vejas () {
    orig=$1
    filename=wap-$1
    time=$(($2 * 3600 * 24))
    width=$3
    title=$4
    db=$5

    rrdtool graph $OUT/$filename \
	-h 50 -w $width -l 0 -s -$time \
	-c BACK#ffffff -c CANVAS#ffffff -c GRID#000000 \
	-c MGRID#000000 -c ARROW#000000 \
	-g \
	DEF:max=$OUT/$db-max.rrd:max:MAX \
	DEF:avg=$OUT/$db-avg.rrd:avg:AVERAGE  \
	DEF:dir=$OUT/$db-dir.rrd:dir:AVERAGE \
	LINE1:max#000000: \
	AREA:avg#000000:

    mogrify -crop 96x60+58+11 $OUT/$filename
    convert $OUT/$filename $OUT/${orig%.png}.wbmp
}


vejas aukst2d.png 2 75 "KOSIS: Aukstadvaris (2 d.)"    aukst
vejas aukst2s.png 14 75 "KOSIS: Aukstadvaris (2 sav.)" aukst

vejas back2d.png 2 75 "KOSIS: Backonys (2 d.)"    back
vejas back2s.png 14 75 "KOSIS: Backonys (2 sav.)" back

vejas didz2d.png 2 75 "KOSIS: Didziulio ez. (2 d.)"    didz
vejas didz2s.png 14 75 "KOSIS: Didziulio ez. (2 sav.)" didz

vejas svent2d.png 2 75 "KOSIS: Sventoji (2 d.)"    svent
vejas svent2s.png 14 75 "KOSIS: Sventoji (2 sav.)" svent

vejas vili2d.png 2 75 "KOSIS: Vilijampole (2 d.)"    vili
vejas vili2s.png 14 75 "KOSIS: Vilijampole (2 sav.)" vili

vejas silute2d.png 2 75 "KOSIS: Silute (2 d.)"    silute
vejas silute2s.png 14 75 "KOSIS: Silute (2 sav.)" silute

vejas klp2d.png 2 75 "KOSIS: Klaipeda (2 d.)"    klp
vejas klp2s.png 14 75 "KOSIS: Klaipeda (2 sav.)" klp


