
from Solutions2019.y2019d5 import y2019d5


def getAllInputs(charSet): #generate all permutations of character set
    charList = []
    inputList = []
    for char in charSet:
        if(char not in inputList):
            charList.append(char)
            inputList.append(char)
    print("Generating with charset" + str(charList))

    roundId = 1
    while(roundId < len(charList)):
        oldInputList = inputList
        inputList = []

        for oldInput in oldInputList:
            for char in charList:
                if(char not in oldInput):
                    inputList.append(char+oldInput)
        
        roundId+=1

    for l in inputList:
        if(inputList.count(l) != 1):
            raise ValueError("Repeated input")

    print("Generated length: " + str(len(inputList)) + ", all verified unique")
    return inputList

def getNextInput(): #just a generator in disguise
    global myInputs
    if(len(myInputs) == 0):
        return None
    
    t = myInputs[0]
    myInputs = myInputs[1:]
    return t

def program(inputString):
    # global inputStr 
    # inputStr = inputString
    i = y2019d5("Input2019/d7.txt", inputString)
    return i

def y2019d7():

    strCpy = None
    maxValue = 0

    myInputs = getAllInputs("01234")

    for inputStr in myInputs:
    
        inputA = [inputStr[0],"0"]
        resA = program(inputA)
        inputB = [inputStr[1],resA]
        resB = program(inputB)
        inputC = [inputStr[2],resB]
        resC = program(inputC)
        inputD = [inputStr[3],resC]
        resD = program(inputD)
        inputE = [inputStr[4],resD]
        resE = program(inputE)

        v = int(resE)

        if(v > maxValue):
            maxValue = v
            maxSet = inputStr

    print("Max value : " + str(maxValue) + " on str " + str(maxSet))
    print("===========")


#part 1 - 182 is wrong
