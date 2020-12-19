# from AOC_Lib.name import *

def y2017d8(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2017/d8.txt"
    print("2017 day 8:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    # for multi line inputs
    conditions = {
        "==" : (lambda x,y : x == y),
        "!=" : (lambda x,y : x != y),
        "<=" : (lambda x,y : x <= y),
        ">=" : (lambda x,y : x >= y),
        "<"  : (lambda x,y : x < y),
        ">"  : (lambda x,y : x > y)
    }

    memory = {}
    maxVal = 0
    for line in lineList:
        s = line.split(" ")
        assert(len(s) == 7)
        
        reg = s[0]
        if reg not in memory:
            memory[reg] = 0
        instr = s[1]
        assert(instr in ["inc", "dec"])
        val = int(s[2])
        condReg = s[4]
        if condReg not in memory:
            memory[condReg] = 0
        condition = s[5]
        assert(condition in conditions)
        condValue = int(s[6])

        if conditions[condition](memory[condReg], condValue):
            memory[reg] += (val * (1 if instr == 'inc' else -1))
            maxVal = max(memory[reg], maxVal)

    Part_1_Answer = max(memory.values())
    Part_2_Answer = maxVal

    return (Part_1_Answer, Part_2_Answer)