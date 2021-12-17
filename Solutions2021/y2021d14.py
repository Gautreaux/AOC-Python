# from AOC_Lib.name import *

from typing import Counter


def y2021d14(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2021/d14.txt"
    print("2021 day 14:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    ex_d = {}

    for p in lineList[2:]:
        k,_,v = p.partition(" -> ")
        ex_d[k] = v

    poly = lineList[0]
    poly_store = {}

    for round_ctr in range(10):
        new_poly = []
        i = iter(poly)
        next(i)

        for l,b in zip(iter(poly), i):
            new_poly.append(l)

            k = l+b

            try:
                new_poly.append(ex_d[k])
            except KeyError:
                pass
        new_poly.append(poly[-1])
        poly = new_poly

        poly_store[round_ctr+1] = poly
    
    def getCount(p):
        c = Counter(p)

        min_c = min(c.items(), key=lambda x: x[1])
        max_c = max(c.items(), key=lambda x: x[1])
        return max_c[1] - min_c[1]

    Part_1_Answer = getCount(poly_store[10])
    # Part_2_Answer = getCount(poly_store[40])

    return (Part_1_Answer, Part_2_Answer)