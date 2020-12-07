# from AOC_Lib.name import *

def y2020d7(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2020/d7.txt"
    print("2020 day 7:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    splitLines = {} # ordered color: [(qty, color)]
    for line in lineList:
        i = line.find("bags contain")
        assert(i > 0)
        inColor = line[:i-1]
        remainder = line[(i + len("bags contain")+1):]
        remainder = remainder.replace(".", ",").replace("bags", "").replace("bag", "").strip()
        assert(remainder[-1] == ',')
        remainderList = []
        while ',' in remainder:
            i = remainder.find(',')
            t = remainder[:i]
            remainder = remainder[i+2:]
            n, c = t.split(" ", 1)
            remainderList.append((n.strip(),c.strip()))

        splitLines[inColor] = remainderList
    
    countedSet = set()
    countedSet.add("shiny gold")
    lastSize = -1

    while True:
        if len(countedSet) == lastSize:
            break
        else:
            lastSize = len(countedSet)
        for bag, contain in splitLines.items():
            for next in contain:
                if next[1] in countedSet:
                    # print(bag)
                    countedSet.add(bag)
        
    Part_1_Answer = len(countedSet) - 1

    # turns out caching doesn't actually make a big difference
    bagCache = {"other": 0}
    def cachedGetBagQty(bagName):
        if bagName in bagCache:
            return bagCache[bagName]

        nextBags = splitLines[bagName]
        thisBags = 0

        for p in nextBags:
            n = p[0]
            if n == "no":
                continue
            b = p[1]
            v = cachedGetBagQty(b)
            thisBags += int(n)*(v+1)

        bagCache[bagName] = thisBags
        return thisBags

    Part_2_Answer = cachedGetBagQty("shiny gold")

    return (Part_1_Answer, Part_2_Answer)