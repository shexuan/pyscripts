#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Remove the read the contains much N or low quality bases. 
Usage:
    python3 QC.py -in fastq1 -out fastq2 -N 0.1 -q 5 -prop 0.5 -stat stat_file 
'''

import sys, os
from collections import defaultdict
import argparse

def qc(fastq_in, fastq_out, N_prop, floor_quality, filter_limit, statistic):
    stat = defaultdict(int)
    with open(fastq_in) as f_in, open(fastq_out,'w') as f_out:
        try:
            while True:
                seq_id = next(f_in)
                seq = next(f_in)
                plus = next(f_in)
                quality = next(f_in)
                stat['raw_reads'] += 1
                cunt_N = seq.count('N')
                stat['N'] += cunt_N
                len_seq = len(seq.strip())
                stat['raw_base'] += len_seq
                q = list(map(lambda x: ord(x), quality.strip()))
                q5 = [i for i in q if i > floor_quality]
                if cunt_N/len_seq < N_prop and len(q5)/len(q) > filter_limit:
                    f_out.write(seq_id)
                    f_out.write(seq)
                    f_out.write(plus)
                    f_out.write(quality)
                    stat['G'] += seq.count('G')
                    stat['C'] += seq.count('C')
                    stat['clean_reads'] += 1
                    stat['clean_base'] += len(seq.strip())
        except StopIteration:
            print('over')
    with open(statistic,'w') as f:
        f.write('raw reads \t\t{}\n'.format(stat['raw_reads']))
        f.write('raw base \t\t{}\n'.format(stat['raw_base']))
        f.write('clean reads \t\t{}\n'.format(stat['clean_reads']))
        f.write('clean base \t\t{}\n'.format(stat['clean_base']))
        f.write('N proportion \t\t{}\n'.format(stat['N']/stat['raw_base']))
        f.write('clean reads proportion \t\t{}\n'.format(stat['clean_reads']/stat['raw_reads']))
        f.write('GC content \t\t{}'.format((stat['G']+stat['C'])/stat['clean_base']))

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-in', type=str, help='Input the raw fastq file')
    parser.add_argument('-out', type=str, help='Output the clean reads')
    parser.add_argument('-stat', type=str, default='{}/stat'.format(os.getcwd()), help='Output the statistics')
    parser.add_argument('-N', type=float, default=0.1, help='Filter the read that "N" content larger than N')
    parser.add_argument('-q', type=int, default=5, help='the base floor quality')
    parser.add_argument('-prop',type=float, default=0.5, help='Filter the reads that the number of bases (quality < floor quality) larger than "-prop"')
    args = vars(parser.parse_args())

    fastq_in = args['in']
    fastq_out = args['out']
    N_prop = args['N']
    floor_quality = args['q']
    filter_limit = args['prop']
    statistic = args['stat']
    
    qc(fastq_in, fastq_out, N_prop, floor_quality, filter_limit, statistic)





