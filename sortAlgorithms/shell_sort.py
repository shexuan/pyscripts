#!/usr/bin/env python3
# coding: utf-8

'''
希尔排序：
这种排序方式基于插入排序，但是一般应用于序列大部分已经排好序的，
这种排序方式一次可以移动多个位置（一次排好一组gap的）。
算法原理参考：http://bubkoo.com/2014/01/15/sort-algorithm/shell-sort/
'''

import random


def shellSort(seq):
    gap = len(seq)//2
    while gap >= 1:
        for i in range(gap, len(seq)):
            idx = i
            # 不仅要将相邻gap的两个数进行比较，还要比较这一组中的所有数
            while idx-gap >= 0:
                if seq[idx] < seq[idx-gap]:
                    seq[idx], seq[idx-gap] = seq[idx-gap], seq[idx]
                    idx -= gap
                else:
                    break
        gap //= 2
    return seq


seq = list(range(100))
random.shuffle(seq)
print(seq)
print(shellSort(seq))
