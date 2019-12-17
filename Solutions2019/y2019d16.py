
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


def y2019d16(inputPath = None):
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
    mul = [None]*inLen
    for i in range(inLen):
        mul[i] = [None]*inLen

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

        
    #now the multiplication matrix is complete
    #the rest is realtively straightforward
    def getNextPhase(sourceList):

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
            tt = str(t)
            outList[i] = int(tt[len(tt)-1])
        
        return outList

    for i in range(100):
        inList = getNextPhase(inList)

    j = ""
    for i in range(8):
        j+=str(inList[i])

    print("Part 1: " + j)
    print("===========")