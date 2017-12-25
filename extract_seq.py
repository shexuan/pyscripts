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
    with open(id_file) as seq_id, open(fasta) as fa, open(result, 'w') as res:
        id_list = [id_.strip() for id_ in seq_id]
        for line in fa:
            if line.startswith('>'):
                for id_ in id_list:
                    if id_ in line:
                        res.write(line)
                        flag = 1
                        n += 1
                        # id_list.remove(id_) #如果id对应的序列唯一的话，取消此行注释可提高效率
                        break
                    else:
                        flag = 0
            else:
                if flag == 1:
                    res.write(line)
    print('over!\n{} sequences has been found!'.format(n))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extracting sequences from fasta according to the seq_id.')
    parser.add_argument('--seqID', '-id', type=str, help='The sequence id to be extracted.')
    parser.add_argument('--fasta', '-fa', type=str, help='The database fasta file.')
    parser.add_argument('-output', '-o', type=str, help='Output the sequence found from fasta.')
    args = vars(parser.parse_args())

    id_file, fasta, result = args['seqID'], args['fasta'], args['output']
    extractSeq(id_file, fasta, result)
