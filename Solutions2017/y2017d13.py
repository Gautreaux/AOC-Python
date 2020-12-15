# from AOC_Lib.name import *

def y2017d13(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2017/d13.txt"
    print("2017 day 13:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    wallsList = []
    for line in lineList:
        s = line.split(": ")
        wallsList.append((int(s[0]), int(s[1])))

    def isAtTopAtTime(range, time) -> bool:
        '''return the true if the range is top at time'''
        if time == 0:
            return True
        period = 2*range - 2
        return time % period == 0
    
    severity = 0
    for wall in wallsList:
        d = wall[0]
        r = wall[1]
        if(isAtTopAtTime(r, d)):
            severity += d*r
    Part_1_Answer = severity


    # TODO - can this be optimized via chinese remainder theorem?


    offset = 0
    while True:
        allGood = True
        for wall in wallsList:
            if isAtTopAtTime(wall[1], offset+wall[0]):
                allGood = False
                break
        if allGood:
            Part_2_Answer = offset
            break
        offset += 1

    return (Part_1_Answer, Part_2_Answer)