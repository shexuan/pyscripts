#!/usr/bin/env python3
# coding: utf-8


import pandas as pd
import numpy as np
import argparse


def density_filter(raw_vcf, density_filtered, step=200, limit=5):
    '''
    filter snp by density.
    if there are over 5 snp in a 200bp window,
    discarding all of them.
    '''
    Chr = ['chr'+str(num) for num in range(1, 23)]+['chrX', 'chrY', 'chrM']
    #all_pos = defaultdict(list)
    all_pos = OrderedDict()
    filter_dict = OrderedDict()
    with open(raw_vcf) as f, open(density_filtered, 'w') as res:
        for line in f:
            if line.startswith('#'):
                res.write(line)
            else:
                all_pos.setdefault(line.split('\t')[0], []).append(
                    int(line.split('\t')[1]))
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
        filtered_snp = [interval for interval,
                        number in density.items() if number <= limit]
        # distribution -> 所有snp位点的分布， filtered_snp -> 密度小于5的snp位点
        filter_dict[chr_] = (distribution, filtered_snp)
    raw_dict = OrderedDict()
    with open(raw_vcf) as f, open(density_filtered, 'a') as res:
        for line in f:
            if not line.startswith('#'):
                s = line.split('\t')
                raw_dict.setdefault(s[0], []).append(line)
        for chr_ in filter_dict:
            for inter, rec in zip(filter_dict[chr_][0], raw_dict[chr_]):
                if inter in filter_dict[chr_][1]:
                    res.write(rec)


def split_info(density_filtered, info_vcf):
    '''
    split vcf INFO column and extract infos.
    '''
    INFO = ['AC', 'AF', 'AN', 'BaseQRankSum', 'ClippingRankSum', 'DP', 'ExcessHet',
            'FS', 'MLEAC', 'MLEAF', 'MQ', 'MQRankSum', 'QD', 'ReadPosRankSum', 'SOR']
    header = '\t'.join((['CHROM', 'POS']+INFO))
    # splited INFO vcf and write to tmp1.info.vcf
    with open(vcf, 'r', encoding='utf-8') as f, open(info_vcf, 'wt', encoding='utf-8') as res:
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


def anno_dbsnpID(dbsnp_ID, info_vcf, anno_snpID_vcf):
    '''
    annotating dbsnp BuildID.
    '''
    vcf = pd.read_csv(info_vcf, header=0, sep='\t')
    cols = ['CHROM', 'POS', 'FS', 'MQ',
            'MQRankSum', 'QD', 'ReadPosRankSum', 'SOR']
    vcf = vcf.loc[:, cols]
    dbsnp = pd.read_csv(dbsnp_ID, header=0, sep='\t')
    dbsnp = dbsnp.loc[:, ('CHROM', 'POS', 'BuildID')]
    # annotate dbsnp BuildID
    vcf_snpID = pd.merge(left=vcf, right=dbsnp,
                         how='left', on=['CHROM', 'POS'])
    # drop duplicated annotated dbsnp ID
    vcf_snpID = vcf_snpID.drop_duplicated(['CHROM', 'POS'])
    # drop un-annotated snp
    vcf_snpID = vcf_snpID.dropna(subset=['BuildID'])
    # fill NA with 0. in col MQRankSum and ReadPosRankSum
    vcf_snpID = vcf_snpID.fillna(0.)
    vcf_snpID.to_csv(anno_snpID_vcf, sep='\t', encoding='utf-8', index=0)


def anno_TP_FP(anno_snpID_vcf, identified_vcf, feature_table):
    '''
    Comparing the raw vcf with identified vcf to marker TP and FP.
    This step can be replace by rtg-tools vcfeval. 
    '''
    vcf_identified = pd.read_csv(
        identified_vcf, header=None, comment='#', sep='\t', usecols=(0, 1, 3))
    vcf_anno_identified = pd.merge(
        anno_snpID_vcf, identified_vcf, how='left', on=['CHROM', 'POS'])
    # mapping matched pos as 1 else 0
    vcf_anno_identified['CLASS'] = vcf_anno_identified['ALT'].apply(
        lambda x: int(1) if isinstance(x, str) else int(0))
    array = (vcf_anno_identified.drop(['CHROM', 'POS', 'ALT'], axis=1))
    # keep 3 digits after the decimal point
    array = array.round(3)
    array.to_csv(feature_table, sep='\t', encoding='utf-8', index=0)


def main():
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Cleanning raw VCF data.")
    parser.add_argument("--raw_vcf", "-r", type="str",
                        help="Input the Raw VCF file.")
    parser.add_argument("--dbsnpID", "-db", type="str",
                        help="Input the dbsnp file.")
    parser.add_argument("--identified_vcf", "-i", type="str",
                        help="Input the identified high confidence VCF file.")
    parser.add_argument('--feature_prefix', '-prefix', type='str',
                        help='The output feature table NAME PREFIX of the raw vcf file, Sample ID recommanded. ')
    args = vars(parser.parse_args())

    # splitted INFO columns and write to tmp1.info.vcf
    info_vcf = 'tmp1.info.vcf'
    # splitted INFO vcf annotated with dbsnp BuildID
    anno_snpID_vcf = 'tmp2.snpID.vcf'
    # density filtered result vcf
    density_filtered = "tmp0.density_filtered.vcf"
    raw_vcf = args['raw_vcf']
    dbsnp_ID = args['dbsnpID']
    identified_vcf = args['identified_vcf']
    feature_table = args['feature_prefix']+'_feature.table'

    main()
