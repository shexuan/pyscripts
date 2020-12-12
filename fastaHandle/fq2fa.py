#!/usr/bin/env python3
# -*- coding: utf-8


'''
transformat fastq file to fasta.
'''
import argparse

def fq2fa(fq, fa):
    n = 0
    with open(fq) as fq, open(fa, 'w') as fa:
        for line in fq:
            if n % 4 == 0:
                line = line.replace("@", ">")
                fa.write(line+'\n')
            if (n-1) % 4 == 0:
                fa.write(line+'\n')
            n += 1
    return None

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="transformat fastq to fasta.")
    parser.add_argument("--fastq","-fq",type=str,help="fastq file to be transformat")
    parser.add_argument("--fasta","-fa",type=str,help="output filename")
    args = vars(parser.parse_args())

    fq = args['fastq']
    fa = args['fasta']
    fq2fa(fq,fa)
