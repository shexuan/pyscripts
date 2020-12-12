#!/usr/bin/env python3
# coding: utf-8

'''
快速排序：
此法用了分治思想，先选择一个基准，然后将序列按此基准不断地成两部分：
大于基准的和小于基准的。因此可用递归解决。
快速排序算法平均时间复杂度为nlgn？
快速排序的效率与基准值的选择有关，若每次选择的基准都是极值，则需递归n此；相反
的，如果每次取的基准都是中间值，则只需递归lgn次。
算法原理参考：http://bubkoo.com/2014/01/12/sort-algorithm/quick-sort/
'''

import random


def quickSort(seq):
    if len(seq) < 2:
        return seq
    else:
        pivot = seq[0]
        less = [i for i in seq[1:] if i <= pivot]
        greater = [i for i in seq[1:] if i > pivot]
        return quickSort(less) + [pivot] + quickSort(greater)


seq = list(range(100))
random.shuffle(seq)
print(seq)
print(quickSort(seq))
