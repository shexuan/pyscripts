#!/usr/bin/env python3
# coding:utf-8

'''
插入排序：
先从序列中选出一个数作为参考（默认序列第一个），
然后将后面的值与第一个（或前面已经排序好的序列）
进行比较，小的插入到已有的大于他的值得前面，大
的插入到最后。
此算法的复杂度依然为n^2。
算法原理参考：http://bubkoo.com/2014/01/14/sort-algorithm/insertion-sort/
'''

import random


def insertionSort(seq):
    sort = [seq[0]]
    for i in range(1, len(seq)):
        for j in range(len(sort)):
            if seq[i] < sort[j]:
                sort.insert(j, seq[i])
                break
        else:
            sort.append(seq[i])
    return sort


seq = list(range(100))
random.shuffle(seq)
print(seq)
print(insertionSort(seq))
