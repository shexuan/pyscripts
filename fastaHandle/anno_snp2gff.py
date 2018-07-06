#!/usr/bin/env python3
# coding: utf-8

'''
annotate the variation position with gff file. 
'''

import sys


def anno_snp(snp_pos, gff, res):
    with open(snp_pos) as snp_f, open(gff) as gf, open(res, 'wt') as res_f:
        snp = []
        for line in snp_f:
            snp_id, Chr, pos, *_ = line.split('\t')
            snp.append((snp_id, Chr, pos))
        anno = []
        for line in gf:
            Chr, _, function, start, end, *_ = line.split('\t')
            anno.append(Chr, function, start, end)
        for s in snp:
            snp_id, snp_Chr, snp_pos = s
            for a in anno:
                anno_Chr, anno_function, anno_start, anno_end = a
                if anno_Chr == snp_Chr and (int(anno_start) <= int(snp_pos) <= int(anno_end)):
                    res_f.write(s+a+'\n')


if __name__ == '__main__':
    snp_pos = sys.argv[1]
    gff = sys.argv[2]
    res = sys.argv[3]
    anno_snp(snp_pos, gff, res)
