
from Solutions2019.y2019d5 import y2019d5
from AOC_Lib.threadedProducerConsumer import ThreadedProducerConsumer
import threading

#TODO - move to lib along with on in 2019d2
class BreakException(Exception):
    pass

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

def program(inputString, inputFunction = None, outputFunction = None):
    # global inputStr 
    # inputStr = inputString
    i = y2019d5("Input2019/d7.txt", inputString, inputFunction, outputFunction)
    return i


def y2019d7():

    strCpy = None
    maxValue = 0

    myInputs = getAllInputs("01234")

    # for inputStr in myInputs:
    
    #     inputA = [inputStr[0],"0"]
    #     resA = program(inputA)
    #     inputB = [inputStr[1],resA]
    #     resB = program(inputB)
    #     inputC = [inputStr[2],resB]
    #     resC = program(inputC)
    #     inputD = [inputStr[3],resC]
    #     resD = program(inputD)
    #     inputE = [inputStr[4],resD]
    #     resE = program(inputE)

    #     v = int(resE)

    #     if(v > maxValue):
    #         maxValue = v
    #         maxSet = inputStr

    # print("Max value (part 1) : " + str(maxValue) + " on str " + str(maxSet))

    phase2Inputs = getAllInputs("56789")

    maxV = 0
    iterCtr = 0

    for p2Input in phase2Inputs:
        lastE = None
        resE = "0"

        aTob = ThreadedProducerConsumer()
        bToc = ThreadedProducerConsumer()
        cTod = ThreadedProducerConsumer()
        dToe = ThreadedProducerConsumer()
        eToa = ThreadedProducerConsumer()

        pcStruct = [aTob, bToc, cTod, dToe, eToa]

        for i in range(len(pcStruct)):
            pcStruct[i].insert(p2Input[i])

        aTob.insert("0")

        threadPool = [None]*len(pcStruct)

        for i in range(len(pcStruct)):
            threadPool[i] = threading.Thread(target = program, args=(None, pcStruct[i].remove, pcStruct[(i+1)%len(pcStruct)].insert))
            threadPool[i].daemon = True
            threadPool[i].start()

        try:
            while(True):


                threadPool[4].join(10)
                break

                #busy spinning!                    
                for i in range(len(pcStruct)):
                    if(pcStruct[i].waitingToRemove != 1):
                        break #one thread is running
                    
                for i in range(len(pcStruct)):
                    if(len(pcStruct[i]) == 0):
                        raise BreakException
                
        except BreakException:
            pass

        v = int(aTob.lastInsert)
        if(v > maxV):
            maxV = v

        # DEBUG
        # print(v)
        # print(p2Input)
        # print(aTob.insertHistory)
        # print(bToc.insertHistory)
        # print(cTod.insertHistory)
        # print(dToe.insertHistory)
        # print(eToa.insertHistory)
        # break

        if(iterCtr %10 ==0):
            print("Iter ctr on " + str(iterCtr))
        iterCtr+=1

    print("Part2: " + str(maxV))


    print("===========")


#part 1 - 182 is wrong
