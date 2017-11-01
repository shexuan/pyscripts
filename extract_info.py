#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pandas as pd
import re


def extract_info(collect_file, seq_file):
    collect_info = pd.read_excel(collect_file, encoding='utf-8',sheetname=0)
    seq_info = pd.read_excel(seq_file, encoding='utf-8',sheetname=1)
    # 注意文库名这一列的格式，如果不含'-'或者含有多个'-',都需要重写匹配 seq_info['libID']
    #seq_info['libID'] = list(map(lambda x, y: x.split(
    #    '-')[0]+'-'+y.split(';')[0]+'-'+y.split(';')[1], seq_info['文库名'], seq_info['QCINDEX']))
    # 这步看情况是用诺和编号还是样品名称来合并，若用样品名称合并注意修改表头使两个表的合并项名称一致
    data3 = pd.merge(collect_info, seq_info, on='诺禾编号')

    sample_list = data3.loc[:, ['LaneID', '结题报告中样品名称',
                                '结题报告中样品名称', '文库名', '诺禾编号', 'INDEX', 'PATH']]
    sample_info = data3.loc[:, ['家系编号', '结题报告中样品名称',
                                '性别（请选择下拉框：M：男／F：女）', '是否患病(请选择下拉框：P：患病 ；N：正常)', '项目编号', 'Disease']]
    sample_info.columns = ['#FamilyID', 'SampleID',
                           'Sex', 'Normal/Patient', 'PN', 'Disease']

    sl_cols = ['LaneID']
    sample_list[sl_cols] = sample_list[sl_cols].astype(int)
    sample_list.columns = ['#LaneID', 'PatientID',
                           'SampleID', 'LibID', 'novoID', 'INDEX', 'PATH']
##########################################################################
######################### 如果是Nova测序的话就有下面这几行，否则的话注释掉 #####################
    nova = sample_list[sample_list.apply(lambda x: True if re.search(
        r'W', x.PATH) else False, axis=1)]
    nova['#LaneID'] = 2
    sample_list = pd.concat([sample_list, nova])
##########################################################################
    return sample_list, sample_info


sample_list, sample_info = extract_info(collect_file=r'C:\Users\sxuan\Desktop\test.xlsx',
                                        seq_file=r'C:\Users\sxuan\Desktop\test.xlsx')

sample_list.to_csv(r'C:\Users\sxuan\Desktop\sample_list_p57.txt',
                   sep='\t', header=True, index=False)
sample_info.to_csv(r'C:\Users\sxuan\Desktop\sample_info_p57.txt',
                   sep='\t', header=True, index=False)
print('finished')
