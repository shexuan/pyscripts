#!/usr/bin/env python3
# coding: utf-8

'''
堆排序：
python中的heapq模块实现了最小堆（也可视为根节点为最小值的完全二叉树）。
在heapq数组中，第一个值始终是最小的。
而且 heap[k] <= heap[2*k+1]，heap[k] <= heap[2*k+2]
算法原理参考：http://bubkoo.com/2014/01/14/sort-algorithm/heap-sort/
'''

import random
from heapq import *


def heapSort(seq):
    heapify(seq)
    return [heappop(seq) for i in range(len(seq))]

seq = list(range(100))
random.shuffle(seq)
print(seq)
print(heapSort(seq))
