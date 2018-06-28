#!/usr/bin/env python3
# coding: utf-8

'''
convert fasta to fastq, all the bases quality assume 40.
'''

import sys


def fa2fq(fasta, fastq):
    with open(fasta) as fa,  open(fastq, 'wt') as fq:
        for line in fa:
            if line.startswith('>'):
                try:
                    # write second line
                    fq.write(sequence+'\n')
                    # third line
                    fq.write('+'+'\n')
                    # fourth line
                    quality = 'I'*len(sequence)
                    fq.write(quality+'\n')
                except:
                    pass
                finally:
                    # first line
                    seq_id = line.replace('>', '@')
                    fq.write(seq_id)
                    # second line
                    sequence = ''
            else:
                sequence += line.strip()
        # 最后一个序列单独写入
        else:
            # write second line
            fq.write(sequence+'\n')
            # third line
            fq.write('+'+'\n')
            # fourth line
            quality = 'I'*len(sequence)
            fq.write(quality+'\n')


if __name__ == '__main__':
    fasta = sys.argv[1]
    fastq = sys.argv[2]
    fa2fq(fasta, fastq)
