import math

def y2019d1(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d1.txt"
    print("2019 day 1:")

    newFuelCounter = 0
    newTotalFuelCounter = 0 #for part 2
    with open(inputPath) as f:
        for line in f:
            newFuelCounter += math.floor(int(line)/3)-2

            tempCtr = int(line)

            while(tempCtr > 0):
                #print(tempCtr)
                newTemp = math.floor(tempCtr/3)-2
                if(newTemp > 0):
                    newTotalFuelCounter += newTemp
                    tempCtr = newTemp
                else:
                    tempCtr = 0

    print("The new fuel needed (part 1) is: " + str(newFuelCounter))
    print("The total new fuel needed (part 2) is: " + str(newTotalFuelCounter))
    print("===========")