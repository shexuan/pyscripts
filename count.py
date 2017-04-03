
import re
import matplotlib.pyplot as plt
import numpy as np
import csv


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

    count = sorted(count.items(), key=lambda d: d[0], reverse=False)
    return count


def LengthToNumbers(file):
    cunt = CountNumbers(file)  # return a tuple, in which every element contains length and numbers.
    length = []
    numbers = []
    for i in range(len(cunt)):
        length.append(cunt[i][0])
        numbers.append(cunt[i][1])
    return length, numbers


numberlist = []
lengthlist = [i for i in range(17, 36)]
filename = ["D:/PY sumbline coding/1MyJob_filtered.txt", "D:/PY sumbline coding/2TS-MyJob_filtered.txt",
            "D:/PY sumbline coding/3MS-MyJob_filtered.txt", "D:/PY sumbline coding/4MF-MyJob_filtered.txt",  "D:/PY sumbline coding/5MG-MyJob_filtered.txt"]

for file in filename:
    length, numbers = LengthToNumbers(file)
    numberlist.append(numbers)

with open(r"D:/PY sumbline coding/count.csv", "a", encoding="utf-8") as cf:
    csvfile = csv.writer(cf)
    csvfile.writerow(lengthlist)
    csvfile.writerows(numberlist)


# visualize these data
with open(r"D:/PY sumbline coding/count.csv","r") as f:
    line=f.readlines()
len_num=[eval(num) for num in line]
x0=np.array(len_num[0])-0.3  # x0-0.3 to put xticks in the bar middle

for i in range(1,6): 
    plt.bar(x0,len_num[i],width=0.15)  # plot one number of length every time 
    x0=x0+0.15 # set every bar width equal to 0.15
    
plt.xticks(range(17,36)) 
plt.xlabel('Length')
plt.ylabel('Numbers')
plt.legend(['f1','f2','f3','f4','f5'])
plt.show()

    