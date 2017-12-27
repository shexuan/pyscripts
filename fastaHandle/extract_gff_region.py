#!/usr/bin/env python3
# coding:utf-8

from collections import defaultdict
import sys


def extractRegion(gff, fasta, out):
    gff_ = defaultdict(list)
    with open(gff, mode='rt') as gf:
        for line in gf:
            tmp = line.strip().split()
            # print(tmp[0])
            # tmp = [seq_id, start, end, gene_id]
            gff_[tmp[0]].append(tmp[1:])
            # gff_ = {seq_id:[start,end,gene_id]}
    with open(fasta) as fa, open(out, 'w') as res:
        for line in fa:
            if line.startswith('>'):
                try:
                    if seq_id in gff_:
                        for record in gff_[seq_id]:
                            start, end, gene_id = record
                            gene_seq = seq[int(start)-1:int(end)+1]
                            res.write('>'+gene_id+'\n')
                            while len(gene_seq) > 100:
                                res.write(gene_seq[0:100] + '\n')
                                gene_seq = gene_seq[100:]
                            res.write(gene_seq[0:100] + '\n')
                except:
                    pass
                finally:
                    seq_id = line.split()[0][1:]
                    # print(seq_id)
                    seq = ''
            else:
                seq += line.strip()
        # for the last seq
        if seq_id in gff_:
            for record in gff_[seq_id]:
                start, end, gene_id = record
                gene_seq = seq[int(start)-1:int(end)+1]
                res.write('>'+gene_id+'\n')
                while len(gene_seq) > 100:
                    res.write(gene_seq[0:100] + '\n')
                    gene_seq = gene_seq[100:]
                res.write(gene_seq[0:100] + '\n')

    print('over')

if __name__ == '__main__':
    gff = sys.argv[1]
    fasta = sys.argv[2]
    out = sys.argv[3]
    extractRegion(gff, fasta, out)
