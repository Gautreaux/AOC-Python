# from AOC_Lib.name import *

# sample variant for reading data from an input file, line by line
def y2018d1(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2018/d1.txt"
    print("2018 day 1:")

    Part_1_Answer = 0
    Part_2_Answer = None

    frequencySet = set()
    freqList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            
            i = int(line[1:])

            if(line[0] == '-'):
                i *= -1

            Part_1_Answer += i
            freqList.append(i)

        k = 0
        f = 0
        while True:
            if f in frequencySet:
                Part_2_Answer = f
                break
            frequencySet.add(f)

            f += freqList[k%len(freqList)]
            k += 1
        
    return (Part_1_Answer, Part_2_Answer)