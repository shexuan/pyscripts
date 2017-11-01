#!/usr/bin/env python3
# -*- coding: utf-8 -*-



# 用两个字典一个字典存chr：position，另一个字典存position：coverage
# 最后将start-end范围内的coverage相加
def combineContinuousSite(file):
    site = defaultdict(list)
    coverage = defaultdict(int)
    with open(file, 'r') as f:
        for line in f:
            pos = line.split()[1]
            site[line.split()[0]].append(int(pos))
            coverage[pos] = line.split()[2]
    return site, coverage


site, coverage = combineContinuousSite(r'C:\Users\sxuan\Desktop\test.txt')
group = defaultdict(list)
group_cover = defaultdict(int)

fun = lambda x: x[1]-x[0]
for chr, pos in site.items():
    for k, g in groupby(enumerate(pos), fun):
        group[chr].append([v for i, v in g])

for chr, g in group.items():       # g -> [[1],[3,4,5]]
    for i in g:
        for pos in i:
            group_cover[str(i)] += int(coverage[str(pos)])

with open(r'C:\Users\sxuan\Desktop\f1.txt', 'w') as f:
    f.write('{0:<4}{1:<10}{2:<10}{3:<8}\n'.format(
        'Chr', 'Start', 'End', 'Cover'))
    for chr, g in group.items():
        g = [str(i) for i in g]
        print(g)
        for pos in g:
            f.write('{0:<4}{1:<10}{2:<10}{3:<8}\n'.format(
                    chr, eval(pos)[0], eval(pos)[-1], group_cover[pos]))
					
					
					
					
