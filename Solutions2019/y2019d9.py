import math

from Solutions2019.y2019d5 import y2019d5

def y2019d9(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d9.txt"
    else:
        print("Using custom path: " + str(inputPath))
    print("2019 day 9:")

    with open(inputPath) as f:
        for line in f:
            #do something
            #TODO - read a single line properly
            myLine = line.strip()
            break
        
        print("Part 1: ", end="")
        print(y2019d5(inputPath, [1]))
        print("Part 2: ", end="")
        print(y2019d5(inputPath, [2]))
    print("===========")


    #incorrect:
    #1091204-1100110011001008100161011006101099
    #2030