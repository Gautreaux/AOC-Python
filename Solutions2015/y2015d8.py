# from AOC_Lib.name import *

def y2015d8(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d8.txt"
    print("2015 day 8:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    total_chars = 0
    total_in_mem = 0
    total_expanded = 0

    for line in lineList:
        assert(line[0] == "\"" and line[-1] == "\"")
        total_chars += len(line)

        s = line[1:-1].replace("\\\\", "S").replace("\\\"", "Q")
        comps = s.split("\\x")

        for i in range(1,len(comps)):
            c = comps[i]
            assert(len(comps) >= 2)
            assert(c[0] in "0123456789abcdef")
            assert(c[1] in "0123456789abcdef")
            comps[i] = "#" + c[2:]
        total_in_mem += sum(map(len, comps))

        s = line.replace("\\", "\\\\").replace("\"","\\\"")
        total_expanded += len(s) + 2 # plus two for new outside ""

    Part_1_Answer = total_chars - total_in_mem
    Part_2_Answer = total_expanded - total_chars

    return (Part_1_Answer, Part_2_Answer)