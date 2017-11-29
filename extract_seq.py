#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Usage:
    python extract_seq.py -id id_file -fa fasta -o output
'''


import argparse


def extractSeq(id_file, fasta, result):
    '''extract sequence from fasta.'''
    flag = 0
    n = 0
    with open(id_file) as seq_id, open(fasta) as fa, open(result, 'wt') as res:
        id_list = (id_ for id_ in seq_id)
        id_dict = dict.fromkeys(id_list, True)
        for line in fa:
            if line.startswith('>'):
                if line[1:] in id_dict:
                    res.write(line)
                    flag = 1
                    n += 1
                    del id_dict[line[1:]]
                else:
                    flag = 0
            else:
                if flag == 1:
                    res.write(line)
    print('over!\n{} sequences has been found!'.format(n))
    for id_ in id_dict:
        print('Cannot find ID:', id_)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extracting sequences from fasta according to the seq_id.')
    parser.add_argument('--seqID', '-id', type=str, help='The sequence id to be extracted.')
    parser.add_argument('--fasta', '-fa', type=str, help='The database fasta file.')
    parser.add_argument('-output', '-o', type=str, help='Output the sequence found from fasta.')
    args = vars(parser.parse_args())

    id_file, fasta, result = args['seqID'], args['fasta'], args['output']
    extractSeq(id_file, fasta, result)
