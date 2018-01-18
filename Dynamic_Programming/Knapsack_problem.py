#!/usr/bin/env python3
# coding: utf-8

'''
goods = [(weight, value), ...]
add a goods for every row to select, 
for example, at row 0, just one goods to select, and row 2, there are another choice... 
so we can format the goods for every row like this:
goods = {0: (1,1500)   # the first row and there only one choice -- to select the goods weight 1 pound and value 1500,
         1: (3,2000)   # the second row, a new goods is added, now there are totally two goods for choice, the new one and the last row goods
         ...}
'''


def KnapsackProblem(row, col):
    # initialize the grid
    grid = [[0]+[1500]*col] + [[0, 1500]+[None]*(col-1) for _ in range(len(row)-1)]
    for i in range(1, len(row)):
        for j in range(1, col+1):
            if j >= goods[i][0]:
                grid[i][j] = max(grid[i-1][j], row[i][1]+grid[i-1][j-row[i][0]])
            else:
                grid[i][j] = grid[i-1][j]
    return grid


raw_goods = [(1, 1500), (4, 3000), (3, 2000), (4, 5000)]
# format goods
goods = {i: raw_goods[i] for i in range(len(raw_goods))}
Knapsack = 4
print(KnapsackProblem(row=goods, col=Knapsack))
print(goods)
