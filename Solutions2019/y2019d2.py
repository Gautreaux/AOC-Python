import math

def getZeroValueFromInput(memoryIn, pos1Value, pos2Value):
    memCpy = [None]*len(memoryIn)
    for i in range(len(memoryIn)):
        memCpy[i] = memoryIn[i]

    memCpy[1] = pos1Value
    memCpy[2] = pos2Value

    return getZeroValue(memCpy)

def getZeroValue(codeInstr):
    myInstr = 0

    while(True):
        operation = codeInstr[myInstr]
        if(operation == 1):
            codeInstr[codeInstr[myInstr+3]] = codeInstr[codeInstr[myInstr+1]] + codeInstr[codeInstr[myInstr+2]]
        elif(operation == 2):
            codeInstr[codeInstr[myInstr+3]] = codeInstr[codeInstr[myInstr+1]] * codeInstr[codeInstr[myInstr+2]]
        elif(operation == 99):
            break
        else:
            raise ValueError("Did not recognize op code " + str(operation) + " at location " + str(myInstr))

        myInstr+=4

    return codeInstr[0]

def y2019d2(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d2.txt"
    print("2019 day 2:")

    with open(inputPath) as f:
        myStr = ""
        for line in f:
            #this is a one line input
            myStr = line.strip()
            break

        myStr += ", "

        #split on commas
        codeInstr = []
        while(myStr.find(",") > 0):
            commaIndex = myStr.find(",")
            codeInstr.append(int(myStr[0:commaIndex]))
            myStr = myStr[commaIndex+1:]

        res = getZeroValueFromInput(codeInstr, 12, 2)

        print("The value in location 0 (part 1) is: " + str(res))

        #part 2
        desiredAnswer = 19690720

        class BreakException(Exception):
            pass

        try:
            for i in range(0, 99):
                for j in range(0, i):
                    res = getZeroValueFromInput(codeInstr, i, j)
                    if(res == desiredAnswer):
                        print("The values for part 2 are: " + str(i) + ", " + str(j))
                        print("The answer is: " + str(i*100+j))
                        raise BreakException
        except BreakException:
            pass

        #part 2 - iterative

        if(99 in codeInstr):
            print("There is a possible reverse solution")
            print("But i'm not going to worry about it because there is only 10000 possible input values")
        else:
            print("The reverse solution is impossible")
    
    print("===========")


#337076 is not correct