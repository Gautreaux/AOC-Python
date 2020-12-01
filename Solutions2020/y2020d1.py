# from AOC_Lib.name import *

# sample variant for reading data from an input file, line by line
def y2020d1(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2020/d1.txt"
    print("2020 day 1:")

    Part_1_Answer = None
    Part_2_Answer = None
    l = []

    with open(inputPath) as f:
        for line in f:
            l.append(int(line.strip()))

    for i in range(len(l)):
        for j in range(i+1, len(l)):
            if l[i] + l[j] == 2020:
                Part_1_Answer = l[i]*l[j]

    for i in range(len(l)):
        for j in range(i+1, len(l)):
            for k in range(j+1, len(l)):
                if l[i] + l[j] + l[k] == 2020:
                    Part_2_Answer = l[i] * l[j] * l[k]
        
    return (Part_1_Answer, Part_2_Answer)
