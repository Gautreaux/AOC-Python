# from AOC_Lib.name import *

# sample variant for reading data from an input file, line by line
from AOC_Lib.npairs import allPairsGenerator, allTriplesGenerator
from AOC_Lib.math import elementwiseMultiplication


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

    for e in allPairsGenerator(l):
        if sum(e) == 2020:
            Part_1_Answer = elementwiseMultiplication(e)

    for e in allTriplesGenerator(l):
        if sum(e) == 2020:
            Part_2_Answer = elementwiseMultiplication(e)
        
    return (Part_1_Answer, Part_2_Answer)
