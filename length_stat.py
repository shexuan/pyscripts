#!/usr/bin/env python3
# coding: utf-8

'''
To stat the length of all seq(contig) in fasta.
'''
import sys
from collections import Counter


def lengthStat(fasta, out):
    length = []
    with open(fasta) as fa:
        for line in fa:
            if line.startswith('>'):
                seq = 0
                length.append(seq)
            else:
                seq += len(line.strip())
    length.append(seq)
    cunt = Counter(length)
    with open(out, 'w') as res:
        for l, n in cunt.items():
            res.write(str(l)+'\t'+str(n)+'\n')


if __name__ == '__main__':
    fasta = sys.argv[1]
    out = sys.argv[2]
    lengthStat(fasta, out)
