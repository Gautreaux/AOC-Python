
#convert the input number to a length 5 representation
def get5LenNumber(inputNum):
    inputNum = str(inputNum)
    while(len(inputNum) < 5):
        inputNum = '0'+inputNum
    return inputNum

#hardcode the input string
# inputStr = "5"
global inputStr
inputStr = "5"

global outputStr
outputStr =  ""

#return and display what the next input will be
def getNextInput():
    global inputStr
    if(inputStr == "" or inputStr == [] or inputStr == None):
        raise ValueError("Asked for more inputs than were specified")
    t = inputStr[0]
    inputStr = inputStr[1:]
    #print("Supplying input: " + str(t))
    return t

def output(strOut):
    global outputStr
    outputStr += str(strOut)

def getParameter(codeInstr, address, mode, relativeBase):
    if(mode == 0):
        return codeInstr[codeInstr[address]]
    elif(mode == 1):
        return codeInstr[address]
    elif(mode == 2):
        #print("MODE2")
        return codeInstr[relativeBase+codeInstr[address]]
    else:
        raise ValueError("Illegal parameter mode " + str(mode))

def y2019d5(inputPath = None, inputString = None, inputFunction = None, outputFunction = None, relativeBase = 0):
    #input function should take no parameters and return a string for the next input
    #output function takes one parameter
    #input str is irrelevant when input function is non-None

    if(inputPath == None):
        inputPath = "Input2019/d5.txt"
    #print("2019 day 5:")

    if(inputString != None):
        global inputStr
        inputStr = inputString
    
    if(inputFunction == None):
        inputFunction = getNextInput
    
    if(outputFunction == None):
        outputFunction = output

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

        global outputStr
        outputStr = ""

        #do the calculation
        myInstr = 0
        while True:
            #i honestly cant explain what is happening in here anymore
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
                codeInstr[codeInstr[myInstr+1]] = int(inputFunction())

                myInstr+=2
            elif(operation == 4):
                param = getParameter(codeInstr, myInstr+1, firstParamMode, relativeBase)
                outputFunction(str(param))

                myInstr+=2
            elif(operation == 1 or operation == 2):
                param = getParameter(codeInstr, myInstr+1, firstParamMode, relativeBase)
                param1 = getParameter(codeInstr, myInstr+2, secondParmaMode, relativeBase)

                if(thirdParamMode != 0):
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
                param = getParameter(codeInstr, myInstr+1, firstParamMode, relativeBase)
                param1 = getParameter(codeInstr, myInstr+2, secondParmaMode, relativeBase)

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
                param = getParameter(codeInstr, myInstr+1, firstParamMode, relativeBase)
                param1 = getParameter(codeInstr, myInstr+2, secondParmaMode, relativeBase)
                
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
            elif(operation == 9):
                param = getParameter(codeInstr, myInstr+1, firstParamMode, relativeBase)
                relativeBase+=param
                myInstr+=2
            else:
                raise ValueError("Illegal operation: " + str(operation) + " in " + str(fiveNum))
        
        
        return outputStr
    print("===========")


#part 2: 14250156 incorrect
# 15386262 -- too high