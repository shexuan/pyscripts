#!/usr/bin/env python3
# coding: utf-8

'''
冒泡排序：
每一次计算都至少能排序出一个最大值，如第一次至少能排好序列最大值，
第二次至少能排好序列第二大值（序列第一大值在第一次已排在最后不用
再次参与排序），后面的亦是如此。
因此,冒泡排序的算法复杂度为n(n+(n-1)+(n-2)+...+1),也即n^2。
算法原理参考：http://bubkoo.com/2014/01/12/sort-algorithm/bubble-sort/
'''


import random
import time


def bubbleSort(seq):
    for j in range(len(seq)-1):
        for i in range(len(seq)-1-j):
            tmp = seq[i]
            if seq[i] > seq[i+1]:
                seq[i] = seq[i+1]
                seq[i+1] = tmp
    return seq

seq = list(range(100))
random.shuffle(seq)

start = time.time()
print(bubbleSort(seq))
end = time.time()
print(end-start)
