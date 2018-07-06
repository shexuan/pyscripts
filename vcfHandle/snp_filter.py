#!/usr/bin/env python3
# coding: utf-8

'''
Filtering snp with density and Kmeans cluster.
'''

# 注： 如果报错，把kmeans_filtered()函数中的R脚本路径换成正确的绝对路径


from collections import OrderedDict, defaultdict, Counter
import os
import sys
from bisect import bisect
#import argparse


def filter_snp(raw_vcf, density_filtered="tmp1.vcf", step=200, limit=5):
    '''
    filter snp by density.
    if there are over 5 snp in a 200bp window,
    discarding all of them.
    '''
    Chr = ['chr'+str(num) for num in range(1, 23)]+['chrX'+'chrY']
    all_pos = defaultdict(list)
    filter_dict = {}
    with open(raw_vcf) as f, open(density_filtered, 'w') as res:
        for line in f:
            if line.startswith('#'):
                res.write(line)
            else:
                all_pos[line.split('\t')[0]].append(int(line.split('\t')[1]))
    for chr_, pos in all_pos.items():
        # 生成所有step区间
        start = pos[0]
        end = pos[-1] + step
        intervals = []
        while start < end:
            intervals.append(start)
            start += step
        # 计算每一个snp掉落在哪一个区间
        distribution = [bisect(intervals, p) for p in pos]
        density = Counter(distribution)
        # interval 表示掉落在第几个区间，number表示掉落在这个区间的snp数量
        filtered_snp = [interval for interval, number in density.items() if number <= limit]
        # distribution -> 所有snp位点的分布， filtered_snp -> 密度小于5的snp位点
        filter_dict[chr_] = (distribution, filtered_snp)
    raw_dict = defaultdict(list)
    with open(raw_vcf) as f, open(density_filtered, 'a') as res:
        for line in f:
            if not line.startswith('#'):
                s = line.split('\t')
                raw_dict[s[0]].append(line)
        for chr_ in filter_dict:
            for inter, rec in zip(filter_dict[chr_][0], raw_dict[chr_]):
                if inter in filter_dict[chr_][1]:
                    res.write(rec)


def split_info(density_filtered):
    '''
    split the INFO column into 15 cols, and filtered some snp without "major info".
    whereafter clustered by Kmeans in R.
    '''
    INFO = ['AC', 'AF', 'AN', 'BaseQRankSum', 'ClippingRankSum', 'DP', 'ExcessHet', 'FS', 'MLEAC', 'MLEAF', 'MQ', 'MQRankSum', 'QD', 'ReadPosRankSum', 'SOR']
    header = '\t'.join((['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'son']+INFO))
    major_info = ['FS', 'MQ', 'MQRankSum', 'QD', 'ReadPosRankSum', 'SOR']
    with open(density_filtered) as f, open('tmp2.vcf', 'w') as res:
        res.write(header+'\n')
        for line in f:
            if not line.startswith('#'):
                INFO_dict = OrderedDict.fromkeys(INFO, 'NA')
                rec = line.split('\t')
                info_col = rec[7]
                info2dict = dict((l.split('=') for l in info_col.split(';')))
                INFO_dict.update(info2dict)
                info_s = '\t'.join(str(val) for key, val in INFO_dict.items())
                res.write(line.strip()+'\t')
                res.write(info_s + '\n')


def kmeans_filter(raw_vcf):
    '''
    split all snp into two classes -- homo and hete. 
    And then clustering with Kmeans in R respectively. 
    Filtering the fake snp with the result of cluster.
    Finally merge them all.
    '''
    os.system('Rscript /home/sxuan/dch/test/kmeans_cluster.r tmp2.vcf')
    with open('density.k2.filtered.vcf', 'w') as res, open('kmeans.filtered.vcf') as f, open(raw_vcf) as raw:
        for line in raw:
            if line.startswith('#'):
                res.write(line)
            else:
                break
        for line in f:
            res.write(line)
    os.remove('tmp1.vcf')
    os.remove('tmp2.vcf')
    os.remove('kmeans.filtered.vcf')


def main(raw_vcf):
    filter_snp(raw_vcf)
    density_filtered = 'tmp1.vcf'
    split_info(density_filtered)
    kmeans_filter(raw_vcf)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description="Filtering snp with density and Kmeans cluster.")
    # parser.add_argument("--in", "-i", type="str", help="raw input vcf file.")
    # args = vars(parser.parse_args())
    # raw_vcf = args["in"]
    arg = sys.argv[1]
    if arg in ['-h', '--help']:
        print("Usage:\tpython snp_filter.py raw.vcf")
    else:
        main(arg)
        print('over')
