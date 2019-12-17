import numpy as np


def constructGenerator(positionIndex):
    assert(positionIndex > 0)
    baseList = [0, 1, 0, -1]
    seqListLen = len(baseList)*positionIndex
    seqList = [None]*seqListLen
    
    for i in range(seqListLen):
        seqList[i] = baseList[i//positionIndex]
    
    t = seqList[0]
    seqList = seqList[1:]
    seqList.append(t)
    

    def genFunction():
        i = 0
        while(True):
            yield seqList[i%(len(seqList))]
            i+=1
    return genFunction

def getMulValue(posX, posY):
    baseList = [0,1,0,-1]
    return baseList[((posX+1)//posY)%4]

def constructMatMul(length):
    #while this works, there is a better way:
    mul = [None]*length
    for i in range(length):
        mul[i] = [None]*length

        #populate this row of the multiplication
        k = constructGenerator(i+1)

        #this doesn't work because of how the variable capture occurred
        # for j in range(len(mul[i])):
        #     t = next(k())
        #     mul[i][j] = next(k())

        #so we get super hacky
        j = 0
        try:
            for t in k():
                mul[i][j] = t
                j+=1
        except IndexError:
            pass
    return mul

    

def getNextPhase(sourceList, mul):
    outList = [None]*len(sourceList)

    assert(len(mul) == len(sourceList))
    
    #loop over the characters one at a time
    for i in range(len(sourceList)):
        #loop over the desired multiplication

        assert(len(mul[i]) == len(sourceList))

        t = 0
        for j in range(len(mul[i])):
            t+= mul[i][j]*sourceList[j]

        #get just the ones digit
        outList[i] = abs(t)%10
    
    return outList

def getNextPhaseV2(sourceList):
    outList = [None]*len(sourceList)

    for i in range(len(sourceList)):
        t = 0
        for j in range(i, len(sourceList)):
            t += getMulValue(j,i+1)*sourceList[j]

        outList[i] = abs(t)%10

        if(len(sourceList) > 1000 and i %500 == 0):
            print(i/len(sourceList))
    return outList

def y2019d16(inputPath = None, doPart2=False):
    if(inputPath == None):
        with open("Input2019/d16.txt") as f:
            inputLine = f.readline().strip()
    else:
        inputLine = inputPath
    
    print("2019 day 16:")

    inList = [None]*len(inputLine)
    inLen = len(inList)

    #break the input into a list
    for i in range(inLen):
        inList[i] = int(inputLine[i])

    #now construct the multiplication matrix
    mul = constructMatMul(inLen)

    #now the multiplication matrix is complete
    #the rest is realtively straightforward

    for i in range(100):
        # inList = getNextPhase(inList, mul)
        inList = getNextPhaseV2(inList)

    j = ""
    for i in range(8):
        j+=str(inList[i])

    print("Part 1: " + j)


    if(not doPart2 and inputPath != None):
        print("===========")
        return

    #construct the super input
    #split into a list
    inListLong = [None]*len(inputLine)*1000
    inLenLong = len(inListLong)

    for i in range(inLenLong):
        inListLong[i] = int(inputLine[i%inLen])
    
    # mulLong = constructMatMul(inLenLong)

    print("Begining the multiplication process")
    for i in range(100):
        inListLong = getNextPhaseV2(inListLong)

        print("==" + str(i) + "== ", end="")

    print("\n\n\n")
    for e in inputLine:
        print(e, end="")
    print("\n")
    offset = int(inputLine[:7])
    j = ""
    for i in range(8):
        j+=str(inList[(i+offset)%inLen])
    print("Part 2: " + j)


    print("===========")