import math

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

        myInstr = 0
        codeInstr[1] = 12
        codeInstr[2] = 2

        while(True):
            operation = codeInstr[myInstr]
            if(operation == 1):
                lhsIndex = codeInstr[myInstr+1]
                lhsValue = codeInstr[lhsIndex]
                rhsIndex = codeInstr[myInstr+2]
                rhsValue = codeInstr[rhsIndex]
                resIndex = codeInstr[myInstr+3]
                codeInstr[resIndex] = lhsValue + rhsValue
                #codeInstr[codeInstr[myInstr+3]] = codeInstr[codeInstr[myInstr+1]] + codeInstr[codeInstr[myInstr+2]]
            elif(operation == 2):
                lhsIndex = codeInstr[myInstr+1]
                lhsValue = codeInstr[lhsIndex]
                rhsIndex = codeInstr[myInstr+2]
                rhsValue = codeInstr[rhsIndex]
                resIndex = codeInstr[myInstr+3]
                codeInstr[resIndex] = lhsValue * rhsValue
                #codeInstr[codeInstr[myInstr+3]] = codeInstr[codeInstr[myInstr+1]] * codeInstr[codeInstr[myInstr+2]]
            elif(operation == 99):
                break
            else:
                raise ValueError("Did not recognize op code " + str(operation) + " at location " + str(myInstr))
        
            myInstr+=4
        
        print("The value in location 0 is " + str(codeInstr[0]))

    print("===========")


#337076 is not correct