#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
remove short reads from fasta file.
Usage:
    python3 rm_short_reads.py -i fasta1 -o fasta2 -l 200
'''

import argparse
from collections import defaultdict


def rmShort(in_file, out_file, length):
    cunt = defaultdict(str)
    with open(in_file) as f_in, open(out_file, 'w') as f_out:
        for line in f_in:
            if line.startswith('>'):
                try:  # 在读取后一条序列的时候处理前一条序列，所以刚刚读取第一行的时候会报错
                    for seq_id, seq in cunt.items():
                        if len(seq) < length:
                            del cunt[seq_id]
                        else:
                            f_out.write(seq_id)
                            f_out.write(seq)
                            del cunt[seq_id]
                except:
                    pass
                finally:
                    id_ = line
            else:
                cunt[id_] += line
        for seq_id, seq in cunt.items():  # 对于最后一行，无法读取其后一行时处理它，故拿出来专门处理
            if len(seq) > length:
                f_out.write(seq_id)
                f_out.write(seq)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, help='Input fasta file')
    parser.add_argument('-o', type=str, help='Output the filtered reads')
    parser.add_argument('-l', type=int, default=200, help='the floor length of the reads')
    args = vars(parser.parse_args())

    in_file = args['i']
    out_file = args['o']
    length = args['l']
    rmShort(in_file, out_file, length)
