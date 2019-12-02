import math

def y2019d1(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d1.txt"
    print("2019 day 1:")

    newFuelCounter = 0
    with open(inputPath) as f:
        for line in f:
            newFuelCounter += math.floor(int(line)/3)-2

    print("The total new fuel needed (part 1) is: " + str(newFuelCounter))

    print("===========")