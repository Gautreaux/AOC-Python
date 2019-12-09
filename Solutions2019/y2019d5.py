
class MemoryModule:
    def __init__(self):
        self.memory = {}

    def __getitem__(self, key):
        if(key < 0):
            raise KeyError("Illegal memory address: " + str(key))
        if(key not in self.memory):
            self.memory[key] = 0
        return self.memory[key]
    
    def __setitem__(self, key, value):
        if(key < 0):
            raise KeyError("Illegal memory address: " + str(key))
        self.memory[key] = value

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
    # print(strOut)
    outputStr += str(strOut) + ", "

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

def writeParameter(codeInstr, address, mode, relativeBase, res):
    if(mode == 0):
        codeInstr[codeInstr[address]] = res
    elif(mode == 2):
        codeInstr[codeInstr[address]+relativeBase] = res
    else:
        raise ValueError("Illegal write parameter mode: " + str(mode))

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
        codeInstr = MemoryModule()
        tempCtr = 0
        while(myStr.find(",") > 0):
            commaIndex = myStr.find(",")
            codeInstr[tempCtr] = (int(myStr[0:commaIndex]))
            tempCtr+=1
            myStr = myStr[commaIndex+1:]

        global outputStr
        outputStr = ""

        #do the calculation
        myInstr = 0
        parameterDict = {1:3,2:3,3:1,4:1,5:2,6:2,7:3,8:3,9:1,99:0}
        while True:
            #i honestly cant explain what is happening in here anymore
            fiveNum = get5LenNumber(codeInstr[myInstr])
            operation = int(fiveNum[3:5])

            if(operation not in parameterDict):
                raise ValueError("Illegal operation: " + str(operation))
            paramCount = parameterDict[operation]

            #memory reset
            if True:
                firstParamMode = None
                secondParmaMode = None
                thirdParamMode = None
                param = None
                param1 = None
                param2 = None

            #parameter setup
            if(paramCount >= 1):
                firstParamMode = int(fiveNum[2])
                param = getParameter(codeInstr, myInstr+1, firstParamMode, relativeBase)
            if(paramCount >= 2):
                secondParmaMode = int(fiveNum[1])
                param1 = getParameter(codeInstr, myInstr+2, secondParmaMode, relativeBase)
            if(paramCount >= 3):
                thirdParamMode = int(fiveNum[0])
                param2 = getParameter(codeInstr, myInstr+3, thirdParamMode, relativeBase)


            if(operation == 99):
                break
            elif(operation == 1):
                writeParameter(codeInstr, myInstr+3, thirdParamMode, relativeBase, param1+param)
            elif(operation == 2):
                writeParameter(codeInstr, myInstr+3, thirdParamMode, relativeBase, param1*param)
            elif(operation == 3):
                writeParameter(codeInstr, myInstr+1, firstParamMode, relativeBase, int(inputFunction()))
            elif(operation == 4):
                outputFunction(str(param))
            elif(operation == 5):
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
            elif(operation == 7):
                if(param < param1):
                    r = 1
                else:
                    r = 0
                writeParameter(codeInstr, myInstr+3, thirdParamMode, relativeBase, r)
            elif(operation == 8):
                if(param == param1):
                    r = 1
                else:
                    r = 0
                writeParameter(codeInstr, myInstr+3, thirdParamMode, relativeBase, r)
            elif(operation == 9):
                relativeBase+=param
            else:
                raise ValueError("Illegal operation: " + str(operation) + " in " + str(fiveNum))
        
            myInstr+=paramCount+1
        
        return outputStr[0:len(outputStr)-2]
    print("===========")


#part 2: 14250156 incorrect
# 15386262 -- too high