#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
remove short reads from fasta file.
Usage:
    python3 rm_short_reads.py -i fasta1 -o fasta2 -l 200
'''

import argparse

def rmShort(in_file, out_file, length):
    out = open(out_file,'w')
    cunt = defaultdict(int)
    total_len = 0
    with open(in_file) as f_in, open(out_file) as f_out:
        for line in f_in:
            if line.startswith('>'):
                try:
                    if len(seq) >= length:
                        f_out.write(seq_id)
                        f_out.write(seq)
                except:
                    pass
                finally:
                    seq_id = line
                    seq = ''
            else: 
                seq += line # 一条序列有多行


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, help='Input fasta file')
    parser.add_argument('-o', type=str, help='Output the filtered reads')
    parser.add_argument('-l', type=int, default=200, help='the floor length of the reads')
    args = vars(parser.parse_args())

    in_file = args['i']
    out_file = args['o']
    length = args['l']
    rmShort(in_file, out_file, length)