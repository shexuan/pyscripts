#!/bin/sh

# author: sxuan
# name: misa_ssr.sh
# function:  identificate and localize perfect microsatellites.
# time: 2017/5/9
# version: 0.1

cd /usr/local/src/misa

for fas 
do
    echo "start running...."
    perl misa.pl $fas
    echo "running over...."
done
