#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gzip
import argparse
import os

'''
Function: remove the polluted reads from genome.
Usage:
python3 filter.py -raw fastq.fq -c rm_list -o out_file
'''

def filterContamination(rm_list, raw_fq, clean_fq):
    f1 = open(rm_list) 
    f2 = gzip.open(raw_fq) 
    f3 = open(clean_fq, 'w')
    # the list of polluted reads id
    rm_list = set([line.strip() for line in f1.readlines()])
    rm_dict = dict.fromkeys(clean_fq_id, True)
    # write the unpolluted reads into a new file
    try:
        while True:
            fq_id = next(f2)
            if fq_id.split()[0] not in rm_dict:
                f3.write(fq_id)
                f3.write(next(f2))
                f3.write(next(f2))
                f3.write(next(f2))
            else:
                next(f2)
                next(f2)
                next(f2)
    except StopIteration:
        print('over')
    f1.close()
    f2.close()
    f3.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This is to clear away the contaminated reads from Genome.')
    parser.add_argument('--RawData','-raw', type=str,
                        help='Input Genome RawDate here.')
    parser.add_argument('--contaminate', '-c', type=str,
                        help='Input the file of contaminated fastq read id here.')
    parser.add_argument('--output', '-o',type=str,
                        help='Output the cleanData here.')
    args = vars(parser.parse_args())
   
    cleanData = args['output']
    raw_fq = args['RawData']
    rm_list = args['contaminate']

    filterContamination(rm_list, raw_fq, cleanData)
