'''
This scripts is to caculate the frequency of diffrent length miRNA in five files.
'''

import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import os


def CountNumbers(file):
    "count the number of different lenth of the sequences."
    with open(r"{}".format(file), "r") as f:  # open files
        reads = f.read()

    pattern = re.compile("[A-Z]+")
    match_list = re.findall(pattern, reads)

    count = dict()
    for i in range(17, 36):
        count[i] = 0
    for read in match_list:
        L = len(read)
        count[L] += 1

    ### a more pythonic method to caculate the number of various length of miRNA in the fasta file
    # from collections import Counter
    # length = [len(seq) for seq in match_list]
    # count = Counter(length)

    count = sorted(count.items(), key=lambda d: d[0], reverse=False)
    return count


def LengthToNumbers(file):
    "return a tuple, in which every element contains length and numbers."
    cunt = CountNumbers(file)
    length = []
    numbers = []
    for i in range(len(cunt)):
        length.append(cunt[i][0])
        numbers.append(cunt[i][1])
    return length, numbers


numberlist = []
lengthlist = [i for i in range(17, 36)]
os.chdir(r"D:/miRNA")
filename = os.listdir()

for file in filename:
    length, numbers = LengthToNumbers(file)
    numberlist.append(numbers)

with open(r"D:/PY sumbline coding/count.csv", "a", encoding="utf-8") as cf:
    csvfile = csv.writer(cf)
    csvfile.writerow(lengthlist)
    csvfile.writerows(numberlist)


# visualize these data
data=pd.read_csv('count.csv').T
data.columns=["F1","F2","F3","F4","F5"]
data.plot.bar(rot=0)
plt.xlabel=("Length of miRNA")
plt.ylabel=("Frequency of Diffrent miRNA")
plt.title("the Number of Various Length of miRNA")
plt.show()
plt.savefig('countFrequency.png',dpi=400,bbox_inches='tight')