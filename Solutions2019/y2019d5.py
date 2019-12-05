import math

# def getZeroValueFromInput(memoryIn, pos1Value, pos2Value):
#     memCpy = [None]*len(memoryIn)
#     for i in range(len(memoryIn)):
#         memCpy[i] = memoryIn[i]

#     memCpy[1] = pos1Value
#     memCpy[2] = pos2Value

#     return getZeroValue(memCpy)

# def getZeroValue(codeInstr):
#     myInstr = 0

#     while(True):
#         operation = codeInstr[myInstr]
#         if(operation == 1):
#             codeInstr[codeInstr[myInstr+3]] = codeInstr[codeInstr[myInstr+1]] + codeInstr[codeInstr[myInstr+2]]
#         elif(operation == 2):
#             codeInstr[codeInstr[myInstr+3]] = codeInstr[codeInstr[myInstr+1]] * codeInstr[codeInstr[myInstr+2]]
#         if(operaiton == 3):
#             codeInstr[codeInstr == ]
#         elif(operation == 99):
#             break
#         else:
#             raise ValueError("Did not recognize op code " + str(operation) + " at location " + str(myInstr))

#         myInstr+=4

#     return codeInstr[0]

def get5LenNumber(inputNum):
    inputNum = str(inputNum)
    while(len(inputNum) < 5):
        inputNum = '0'+inputNum
    return inputNum

inputStr = "5"
def getNextInput():
    global inputStr
    if(inputStr == ""):
        raise ValueError("Asked for more inputs than were specified")
    t = inputStr[0]
    inputStr = inputStr[1:]
    print("Supplying input: " + str(t))
    return t

def y2019d5(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d5.txt"
    print("2019 day 5:")

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

        #do the calculation
        myInstr = 0
        while True:
            fiveNum = get5LenNumber(codeInstr[myInstr])
            operation = int(fiveNum[3:5])

            firstParamMode = int(fiveNum[2])
            secondParmaMode = int(fiveNum[1])
            thirdParamMode = int(fiveNum[0])

            if(operation == 99):
                break
            elif(operation == 3):
                # if(firstParamMode == 1):
                #     param = codeInstr[(myInstr+1)]
                # else:
                #     param = codeInstr[codeInstr[myInstr+1]]
                #param = codeInstr[codeInstr[(myInstr+1)]]
                codeInstr[codeInstr[myInstr+1]] = int(getNextInput())

                myInstr+=2
            elif(operation == 4):
                if(firstParamMode == 1):
                    param = codeInstr[(myInstr+1)]
                else:
                    param = codeInstr[codeInstr[myInstr+1]]
                # param = codeInstr[(myInstr+1)]
                print(param)

                myInstr+=2
            elif(operation == 1 or operation == 2):
                if(firstParamMode == 1):
                    param = codeInstr[(myInstr+1)]
                else:
                    param = codeInstr[codeInstr[(myInstr+1)]]

                if(secondParmaMode == 1):
                    param1 = codeInstr[(myInstr+2)]
                else:
                    param1 = codeInstr[codeInstr[(myInstr+2)]]

                if(thirdParamMode == 1):
                    raise Exception("Writes should not be in immediate mode")
                    #param2 = codeInstr[(myInstr+3)]
                else:
                    param2 = codeInstr[codeInstr[(myInstr+3)]]

                if(operation == 1):
                    res = param1 + param
                elif(operation == 2):
                    res = param1 * param
                else:
                    raise ValueError

                codeInstr[codeInstr[(myInstr+3)]] = res

                myInstr+=4
            elif(operation == 5 or operation == 6):
                if(firstParamMode == 1):
                    param = codeInstr[(myInstr+1)]
                else:
                    param = codeInstr[codeInstr[(myInstr+1)]]

                if(secondParmaMode == 1):
                    param1 = codeInstr[(myInstr+2)]
                else:
                    param1 = codeInstr[codeInstr[(myInstr+2)]]

                if(operation == 5):
                    if(param != 0):
                        myInstr = param1
                        continue
                    else:
                        pass
                elif(operation == 6):
                    if(param == 0):
                        myInstr = param1
                        continue
                    else:
                        pass

                myInstr+=3
            elif(operation == 7 or operation == 8):
                if(firstParamMode == 1):
                    param = codeInstr[(myInstr+1)]
                else:
                    param = codeInstr[codeInstr[(myInstr+1)]]

                if(secondParmaMode == 1):
                    param1 = codeInstr[(myInstr+2)]
                else:
                    param1 = codeInstr[codeInstr[(myInstr+2)]]
                
                # if(thirdParamMode == 1):
                #     param2 = codeInstr[(myInstr+3)]
                # else:
                #     param2 = codeInstr[codeInstr[(myInstr+3)]]
                param2 = codeInstr[(myInstr+3)]

                if(operation == 7):
                    if(param < param1):
                        codeInstr[param2] = 1
                    else:
                        codeInstr[param2] = 0
                elif(operation == 8):
                    if(param == param1):
                        codeInstr[param2] = 1
                    else:
                        codeInstr[param2] = 0

                myInstr+=4

            else:
                raise ValueError("Illegal operation: " + str(operation) + " in " + str(fiveNum))


        # print("The value in location 0 (part 1) is: " + str(res))

        #part 2
    
    print("===========")


#part 2: 14250156 incorrect
# 15386262 -- too high