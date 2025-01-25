# from AOC_Lib.name import *


def y2021d1(inputPath=None):
    if inputPath == None:
        inputPath = "Input2021/d1.txt"
    print("2021 day 1:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    i_list = list(map(int, lineList))

    itr = iter(i_list)
    next(itr)

    Part_1_Answer = len(list(filter(lambda x: x[0] < x[1], zip(i_list, itr))))

    itr = iter(i_list)
    next(itr)

    itr_2 = iter(i_list)
    next(itr_2)
    next(itr_2)

    window_sums = list(map(sum, zip(i_list, itr, itr_2)))

    itr = iter(window_sums)
    next(itr)
    Part_2_Answer = len(list(filter(lambda x: x[0] < x[1], zip(window_sums, itr))))

    return (Part_1_Answer, Part_2_Answer)
