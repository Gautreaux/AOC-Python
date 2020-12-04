# from AOC_Lib.name import *

# sample variant for reading data from an input file, line by line
def y%{year}d%{day}(inputPath = None):
    if(inputPath == None):
        inputPath = "Input%{year}/d%{day}.txt"
    print("%{year} day %{day}:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    # for single line inputs
    for c in lineList[-1]:
        pass

    # for multi line inputs

    return (Part_1_Answer, Part_2_Answer)