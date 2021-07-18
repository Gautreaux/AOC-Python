# from AOC_Lib.name import *

from hashlib import md5

def y2015d4(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d4.txt"
    print("2015 day 4:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    myKey = lineList[0]

    for i in range(10000000000):
        v = md5((myKey + str(i)).encode("ascii")).hexdigest()
        if v[:5] == "00000":
            Part_1_Answer = i

            if v[:6] == "000000":
                Part_2_Answer = i
            break
        
        if i%100000 == 0:
            print(f"i = {i}")
    
    for i in range(Part_1_Answer, 10000000000):
        v = md5((myKey + str(i)).encode("ascii")).hexdigest()

        if v[:6] == "000000":
            Part_2_Answer = i
            break
        
        if i%100000 == 0:
            print(f"i = {i}")

    return (Part_1_Answer, Part_2_Answer)