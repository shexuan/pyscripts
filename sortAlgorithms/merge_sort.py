#!/usr/bin/env python3
# coding: utf-8


'''
归并排序：
也是基于分治思想，将序列不断分解后排序重新逐个合并小序列。
在实现上与快速排序非常像。
算法原理参考：http://bubkoo.com/2014/01/15/sort-algorithm/merge-sort/
部分代码参考：http://zh.wikipedia.org/zh/%E5%BD%92%E5%B9%B6%E6%8E%92%E5%BA%8F
'''
import random


def mergeSort(seq):
    if len(seq) <= 1:
        return seq
    left = mergeSort(seq[:len(seq)//2])
    right = mergeSort(seq[len(seq)//2:])
    return merge(left, right)
    # 也可用直接用heapq模块的merge函数
    # import heapq
    # return list(heapq.merge(left, right))


def merge(left, right):
    sort = []
    while left and right:
        sort.append(left.pop(0) if left[0] <= right[0] else right.pop(0))
    if left:
        sort.extend(left)
    if right:
        sort.extend(right)
    return sort


seq = list(range(100))
random.shuffle(seq)
print(seq)
print(mergeSort(seq))
