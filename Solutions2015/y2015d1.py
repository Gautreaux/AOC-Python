# from AOC_Lib.name import *


# sample variant for reading data from an input file, line by line
def y2015d1(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d1.txt"
    print("2015 day 1:")

    Part_1_Answer = None
    Part_2_Answer = None

    with open(inputPath) as f:
        for line in f:
            # there should be only one line
            line = line.strip()
            depth = 0
            index = 0
            for c in line:
                index += 1
                if c == '(':
                    depth += 1
                elif c == ')':
                    depth -= 1
                else:
                    raise ValueError(f"Unrecognized character: '{c}'")
                if depth < 0 and Part_2_Answer is None:
                    Part_2_Answer = index
            Part_1_Answer = depth
            break
        
    return (Part_1_Answer, Part_2_Answer)