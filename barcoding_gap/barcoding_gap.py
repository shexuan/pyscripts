#!/usr/bin/env python3
# coding: utf-8

import csv
from collections import defaultdict

albus = list(range(5))
bulbifer = list(range(5, 10))
konjac = list(range(10, 15))
muelleri = list(range(15, 21))
yulo = list(range(21, 26))

amor = {"albus": list(range(5)), "bulbifer": list(range(5, 10)), "muelleri": list(range(10, 16)), "yulo": list(range(16, 20))}


def intra_and_inter_distance(file, genus):
    dist_arr = []
    intra_dist = defaultdict(list)
    inter_dist = []
    with open(file) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            dist_arr.append(row)
    # print(dist_arr)
    #print(len(dist_arr), len(dist_arr[-1]))
    for i in range(1, 25):
        for j in range(i):
            for spe in amor:
                species = amor[spe]
                if i in species and j in species:
                    intra_dist[spe].append(float(dist_arr[i][j]))
                    break
                if i in species and j not in species:
                    #print(i, j)
                    # print(dist_arr[i][j])
                    inter_dist.append(float(dist_arr[i][j]))
                    break
    max_intra_dist = {spe: max(intra_dist[spe]) for spe in intra_dist}
    min_inter_dist = min(inter_dist)
    avg_inter_dist = sum(inter_dist)/len(inter_dist)
    return max_intra_dist, min_inter_dist, avg_inter_dist


import os
os.chdir(r'D:\毕业实验\DNA条形码\条形码合并')

file = r'Flint2\Distance_Data.csv'
max_intra, min_inter, avg_inter = intra_and_inter_distance(file=file, genus=amor)
print(max_intra, min_inter, avg_inter)
