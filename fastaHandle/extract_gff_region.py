#!/usr/bin/env python3
# coding:utf-8

'''
Extract gene seq from ref.fa according to the gff. 
Usage:
    python3 extract_gff_region.py gff ref.fa out
'''

from collections import defaultdict
import argparse


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
    parser = argparse.ArgumentParser(description='Extract gene seq from ref.fa according to the gff')
    parser.add_argument('-gff', type=str, help='Input the gff file')
    parser.add_argument('-out', '-o' type=str, help='Output gene and sequence')
    parser.add_argument('-fa', '--fasta', type=float, default=0.5, help='reference genome file')
    args = vars(parser.parse_args())

    gff = args['gff']
    fasta = args['fasta']
    out = args['out']
    extractRegion(gff, fasta, out)
