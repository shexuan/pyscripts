#!/usr/bin env python3
# coding: utf-8

'''
split the INFO clomun of vcf file.  
'''

from collections import OrderedDict
import sys


def split_info(vcf):
    INFO = ['AC', 'AF', 'AN', 'BaseQRankSum', 'ClippingRankSum', 'DP', 'ExcessHet',
            'FS', 'MLEAC', 'MLEAF', 'MQ', 'MQRankSum', 'QD', 'ReadPosRankSum', 'SOR']
    header = '\t'.join((['CHROM', 'POS']+INFO))
    with open(vcf, 'r', encoding='utf-8') as f, open(vcf+'.info', 'w', encoding='utf-8') as res:
        res.write(header+'\n')
        for line in f:
            if not line.startswith('#'):
                INFO_dict = OrderedDict.fromkeys(INFO, 'NA')
                rec = line.split('\t')
                info_col = rec[7]
                info2dict = dict((l.split('=') for l in info_col.split(';')))
                INFO_dict.update(info2dict)
                info_s = '\t'.join(str(val) for key, val in INFO_dict.items())
                res.write(rec[0]+'\t'+rec[1]+'\t')
                res.write(info_s + '\n')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Usage:\tpython3 split_info VCF.file')
    else:
        split_info(sys.argv[1])
