#!/usr/bin/env python3
# coding: utf-8

'''
选择排序：
每一次遍历都从序列中找出最小值（最大值），插入到序列的最前端。
理论上在算法复杂度上面可以说是与冒泡排序差不多的，都是n^2。
算法原理参考：http://bubkoo.com/2014/01/13/sort-algorithm/selection-sort/
'''
import random


def selectSort(seq):
    sort = []
    for j in range(len(seq)-1):
        smallest = seq[0]
        smallest_index = 0
        for i in range(1, len(seq)):
            if smallest > seq[i]:
                smallest = seq[i]
                smallest_index = i
        sort.append(seq.pop(smallest_index))
    sort.extend(seq)
    return sort


seq = list(range(100))
random.shuffle(seq)
print(seq)
print(selectSort(seq))
