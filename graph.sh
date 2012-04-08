#!/bin/sh

# C3 is 2-3 m/s
# C4 is 3-4 m/s
#C0='#9600fe'
C1='#6400fe'
C2='#3200fe'
C3='#0032fe'
C4='#0064fe'
C5='#0096fe'
C6='#00c8fe'
C7='#00e6f0'
C8='#00e6a0'
C9='#00e677'
C10='#00e650'
C11='#00f028'
C12='#00fa00'
C13='#fefe00'
C14='#fee100'
C15='#fec800'
C16='#feae00'
C17='#fe9600'
C18='#e67d00'
C19='#e66400'
C20='#dc4a1d'

S="#0000FF"
SR="#00bfff"
R="#00fe2a"
PR="#bfff00"
P="#ffff00"
PV="#ff6a00"
V="#ff0055"
SV="#bf00ff"

vejas () {
    filename=$1
    time=$(($2 * 3600 * 24))
    width=$3
    height=$4
    title=$5
    db=$6

    rrdtool graph $OUT/$filename \
	-v 'Vejas, m/s'  \
	-h $height -w $width -l 0 -s -$time -t "$title" \
	DEF:max=$OUT/$db-max.rrd:max:MAX \
	DEF:avg=$OUT/$db-avg.rrd:avg:AVERAGE  \
	DEF:dir=$OUT/$db-dir.rrd:dir:AVERAGE \
	CDEF:background=dir,POP,TIME,14400,%,7200,LT,INF,UNKN,IF \
	CDEF:avg1=avg,1,LT,avg,UNKN,IF \
	CDEF:avg2=avg,2,LT,avg,UNKN,IF \
	CDEF:avg3=avg,3,LT,avg,UNKN,IF \
	CDEF:avg4=avg,4,LT,avg,UNKN,IF \
	CDEF:avg5=avg,5,LT,avg,UNKN,IF \
	CDEF:avg6=avg,6,LT,avg,UNKN,IF \
	CDEF:avg7=avg,7,LT,avg,UNKN,IF \
	CDEF:avg8=avg,8,LT,avg,UNKN,IF \
	CDEF:avg9=avg,9,LT,avg,UNKN,IF \
	CDEF:avg10=avg,10,LT,avg,UNKN,IF \
	CDEF:avg11=avg,11,LT,avg,UNKN,IF \
	CDEF:avg12=avg,12,LT,avg,UNKN,IF \
	CDEF:avg13=avg,13,LT,avg,UNKN,IF \
	CDEF:avg14=avg,14,LT,avg,UNKN,IF \
	CDEF:avg15=avg,15,LT,avg,UNKN,IF \
	CDEF:avg16=avg,16,LT,avg,UNKN,IF \
	CDEF:avg17=avg,17,LT,avg,UNKN,IF \
	CDEF:avg18=avg,18,LT,avg,UNKN,IF \
	CDEF:avg19=avg,19,LT,avg,UNKN,IF \
	CDEF:avg20=avg \
	CDEF:max1=max,1,LT,max,UNKN,IF \
	CDEF:max2=max,2,LT,max,UNKN,IF \
	CDEF:max3=max,3,LT,max,UNKN,IF \
	CDEF:max4=max,4,LT,max,UNKN,IF \
	CDEF:max5=max,5,LT,max,UNKN,IF \
	CDEF:max6=max,6,LT,max,UNKN,IF \
	CDEF:max7=max,7,LT,max,UNKN,IF \
	CDEF:max8=max,8,LT,max,UNKN,IF \
	CDEF:max9=max,9,LT,max,UNKN,IF \
	CDEF:max10=max,10,LT,max,UNKN,IF \
	CDEF:max11=max,11,LT,max,UNKN,IF \
	CDEF:max12=max,12,LT,max,UNKN,IF \
	CDEF:max13=max,13,LT,max,UNKN,IF \
	CDEF:max14=max,14,LT,max,UNKN,IF \
	CDEF:max15=max,15,LT,max,UNKN,IF \
	CDEF:max16=max,16,LT,max,UNKN,IF \
	CDEF:max17=max,17,LT,max,UNKN,IF \
	CDEF:max18=max,18,LT,max,UNKN,IF \
	CDEF:max19=max,19,LT,max,UNKN,IF \
	CDEF:max20=max \
	CDEF:ddir=dir,22.5,/ \
	CDEF:gap=-0.5,-0.5,dir,IF \
	CDEF:dirs2=dir,360,LE,avg,-1,MIN,UNKN,IF \
	 CDEF:dirs=dir,avg,5,/,GT,avg,-1,MIN,UNKN,IF \
	CDEF:dirsr=dir,22.5,GT,avg,-1,MIN,UNKN,IF \
	 CDEF:dirr=dir,67.5,GT,avg,-1,MIN,UNKN,IF \
	CDEF:dirpr=dir,112.5,GT,avg,-1,MIN,UNKN,IF \
	 CDEF:dirp=dir,157.5,GT,avg,-1,MIN,UNKN,IF \
	CDEF:dirpv=dir,220.5,GT,avg,-1,MIN,UNKN,IF \
	 CDEF:dirv=dir,247.5,GT,avg,-1,MIN,UNKN,IF \
	CDEF:dirsv=dir,292.5,GT,avg,-1,MIN,UNKN,IF \
	LINE1:max$C10: \
	LINE1:max20$C20:  \
	LINE1:max19$C19:  \
	LINE1:max18$C18:  \
	LINE1:max17$C17:  \
	LINE1:max16$C16:  \
	LINE1:max15$C15:  \
	LINE1:max14$C14:  \
	LINE1:max13$C13:  \
	LINE1:max12$C12:  \
	LINE1:max11$C11:  \
	LINE1:max10$C10:  \
	LINE1:max9$C9: \
	LINE1:max8$C8: \
	LINE1:max7$C7: \
	LINE1:max6$C6: \
	LINE1:max5$C5: \
	LINE1:max4$C4: \
	LINE1:max3$C3: \
	LINE1:max2$C2: \
	LINE1:max1$C1: \
	AREA:avg$C5:  \
	AREA:avg20$C20:  \
	AREA:avg19$C19:  \
	AREA:avg18$C18:  \
	AREA:avg17$C17:  \
	AREA:avg16$C16:  \
	AREA:avg15$C15:  \
	AREA:avg14$C14:  \
	AREA:avg13$C13:  \
	AREA:avg12$C12:  \
	AREA:avg11$C11:  \
	AREA:avg10$C10:  \
	AREA:avg9$C9: \
	AREA:avg8$C8: \
	AREA:avg7$C7: \
	AREA:avg6$C6: \
	AREA:avg5$C5: \
	AREA:avg4$C4: \
	AREA:avg3$C3: \
	AREA:avg2$C2: \
	AREA:avg1$C1: \
	COMMENT:\\s \
	COMMENT:\\s \
	COMMENT:\\s \
	COMMENT:"Vejo kryptis" \
	HRULE:0#000000: \
	AREA:gap\#FFFFFF: \
	STACK:dirs$S:S \
	AREA:gap: \
	STACK:dirs2$S: \
	AREA:gap: \
	STACK:dirsr$SR:SR \
	AREA:gap: \
	STACK:dirr$R:R \
	AREA:gap: \
	STACK:dirpr$PR:PR \
	AREA:gap: \
	STACK:dirp$P:P \
	AREA:gap: \
	STACK:dirpv$PV:PV \
	AREA:gap:  \
	STACK:dirv$V:V \
	AREA:gap: \
	STACK:dirsv$SV:SV \
	#HRULE:6\#FF0000:"Rock'n'roll"
	#LINE1:max$C10:Maksimalus \
        #AREA:avg$C5:Vidutinis  \
}

kryptis () {
    rrdtool graph $OUT/kryptis.png \
        -v 'Vejas, kryptis' "$@" \
        -h 100 -w 400 \
        -l 0 -u 360 -r \
        -y 45:2  \
        -s -200000 -t "KOSIS: Aukstadvaris" \
        DEF:dir=$OUT/aukst-dir.rrd:dir:AVERAGE \
        CDEF:dirs2=dir,360,LE,dir,UNKN,IF \
        CDEF:dirs=dir,0,GT,dir,UNKN,IF \
        CDEF:dirsr=dir,22.5,GT,dir,UNKN,IF \
        CDEF:dirr=dir,67.5,GT,dir,UNKN,IF \
        CDEF:dirpr=dir,112.5,GT,dir,UNKN,IF \
        CDEF:dirp=dir,157.5,GT,dir,UNKN,IF \
        CDEF:dirpv=dir,220.5,GT,dir,UNKN,IF \
        CDEF:dirv=dir,247.5,GT,dir,UNKN,IF \
        CDEF:dirsv=dir,292.5,GT,dir,UNKN,IF \
        "COMMENT:Vejo kryptis" \
        LINE2:dirs$S:S \
        LINE2:dirs2$S: \
        LINE2:dirsr$SR:SR \
        LINE2:dirr$R:R \
        LINE2:dirpr$PR:PR \
        LINE2:dirp$P:P \
        LINE2:dirpv$PV:PV \
        LINE2:dirv$V:V \
        LINE2:dirsv$SV:SV
}

OUT=${1:-.}

vejas aukst2d.png 2 400 200 "KOSIS: Aukstadvaris (2 d.)"    aukst
vejas aukst2s.png 14 675 200 "KOSIS: Aukstadvaris (2 sav.)" aukst

vejas back2d.png 2 400 200 "KOSIS: Backonys (2 d.)"    back
vejas back2s.png 14 675 200 "KOSIS: Backonys (2 sav.)" back

vejas didz2d.png 2 400 200 "KOSIS: Didziulio ez. (2 d.)"    didz
vejas didz2s.png 14 675 200 "KOSIS: Didziulio ez. (2 sav.)" didz

vejas svent2d.png 2 400 200 "KOSIS: Sventoji (2 d.)"    svent
vejas svent2s.png 14 675 200 "KOSIS: Sventoji (2 sav.)" svent

vejas vili2d.png 2 400 200 "KOSIS: Vilijampole (2 d.)"    vili
vejas vili2s.png 14 675 200 "KOSIS: Vilijampole (2 sav.)" vili

vejas silute2d.png 2 400 200 "KOSIS: Silute (2 d.)"    silute
vejas silute2s.png 14 675 200 "KOSIS: Silute (2 sav.)" silute

vejas klp2d.png 2 400 200 "KOSIS: Klaipeda (2 d.)"    klp
vejas klp2s.png 14 675 200 "KOSIS: Klaipeda (2 sav.)" klp

# Delninis formatas
vejas aukst2dm.png 2 150 100 "KOSIS: Aukstadvaris (2 d.)"    aukst
vejas back2dm.png 2 150 100 "KOSIS: Backonys (2 d.)"    back
vejas didz2dm.png 2 150 100 "KOSIS: Didziulio ez. (2 d.)"    didz
vejas svent2dm.png 2 150 100 "KOSIS: Sventoji (2 d.)"    svent
vejas vili2dm.png 2 150 100 "KOSIS: Vilijampole (2 d.)"    vili
vejas silute2dm.png 2 150 100 "KOSIS: Silute (2 d.)"    silute
vejas klaipeda2dm.png 2 150 100 "KOSIS: Klaipeda (2 d.)"    klp

# VG grafikas
vejas aukstvg.png 2 115 80 "Aukstadvaris" aukst
mogrify -crop 151x105+40+25 $OUT/aukstvg.png

# Do the  wireless thing, too!
exec ./wbmp.sh $OUT
