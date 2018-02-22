#!/usr/bin/env python3
# coding: utf-8


def binary_search(target, arr):
    # 折半查找
    low = 0
    high = len(arr)-1
    while low <= high:
        mid = (low+high)//2
        if target > arr[mid]:
            low = mid+1
        elif target < arr[mid]:
            high = mid-1
        else:
            return mid, arr[mid]


def insert_search(target, arr):
    # 插值查找，改变了mid的公式，不再是简简单单的1/2
    low = 0
    high = len(arr)-1
    while low <= high:
        mid = low + ((target-arr[low])//(arr[high]-arr[low]))*(high-low)
        if target > arr[mid]:
            low = mid+1
        elif target < arr[mid]:
            high = mid-1
        else:
            return mid, arr[mid]


def fibonacci_search(target, arr):
    # 斐波那契查找
    # 生成斐波那契数列
    fib = [0, 1]
    for i in range(1, 33):
        fib.append(fib[-1]+fib[-2])
    # 确定查找数组长度在斐波那契数列的位置
    k = 0
    n = len(arr)
    while n > fib[k]-1:
        k += 1
    # 将待查找数组扩充到指定长度
    for i in range(n, fib[k]):
        arr.append(arr[-1])

    low, high = 0, n-1
    while low <= high:
        mid = low+fib[k-1]-1
        if target < arr[mid]:
            high = mid-1
            k = k-1
        elif target > arr[mid]:
            low = mid+1
            k = k-2
        else:
            if mid < n:
                return mid
            else:
                return n-1


arr = [1, 2, 3, 34, 56, 57, 78, 87]
print(fibonacci_search(57, arr))
