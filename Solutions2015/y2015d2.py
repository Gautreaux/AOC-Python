# from AOC_Lib.name import *
import re

# sample variant for reading data from an input file, line by line
def y2015d2(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d2.txt"
    print("2015 day 2:")

    Part_1_Answer = None
    Part_2_Answer = None

    paperFootage = 0
    ribbonFootage = 0

    with open(inputPath) as f:
        for line in f:
            x = re.search("([0-9]*)x([0-9]*)x([0-9]*)", line)
            
            if x is None:
                raise ValueError(f"Regex failed on line {line}")
            a = int(x.group(1))
            b = int(x.group(2))
            c = int(x.group(3))
            k = [a*b, b*c, a*c]
            paperFootage += 2*sum(k) + min(k)

            v = [a,b,c]
            v.sort()
            ribbonFootage += 2*(v[0] + v[1]) + (a*b*c)


        
    Part_1_Answer = paperFootage
    Part_2_Answer = ribbonFootage
    return (Part_1_Answer, Part_2_Answer)