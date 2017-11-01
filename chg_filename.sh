#!/bin/bash

# author: sxuan
# name: chg_file_name.sh
# time: 2017/5/1
# function: Change a suffix to files in DIR.  
# version: 0.1

DIR=$1
old=$2
new=$3

if [ $1 == "-h" -o $1 == "--help" ]; then 
    echo "Usage:"
    echo "chg_filename absolute_dir old_suffix new_suffix"

else
    for file in `ls $DIR | grep "$old"`
    do
        new_name=$(echo $file | sed "s/\.$old/\.$new/")
        mv $file $new_name
    done
fi
