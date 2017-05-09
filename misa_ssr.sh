#!/usr/bin/sh

# author: sxuan
# name: misa_ssr.sh
# function:  identificate and localize perfect microsatellites.
# time: 2017/5/9
# version: 0.0

FasDir=/home/sxuan/local
cd /usr/local/src/misa

for fas in `ls $FasDir`
do
    perl misa.pl $fas
done
