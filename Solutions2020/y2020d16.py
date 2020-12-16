# from AOC_Lib.name import *
import itertools
from copy import deepcopy

def y2020d16(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2020/d16.txt"
    print("2020 day 16:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    type1Lies = []
    myticket = None
    nearby = []
    
    for l in lineList:
        
        if l in ["", "your ticket:", "nearby tickets:"]:
            continue
        i = l.find("or")
        if i != -1:
            type1Lies.append(l)
        else:
            if myticket is None:
                myticket = l
            else:
                nearby.append(l)

    # print(type1Lies)
    # print(myticket, end = "\n\n\n\n\n\n")
    # print(nearby)

    fields = {}

    def splitInt(s):
        s = s.strip()
        k = s.split("-")
        return (int(k[0]), int(k[1]))

    for c in type1Lies:
        s = c.split(":")
        name = s[0]
        s = s[1].strip().split(" or ")
        fields[name] = (splitInt(s[0]), splitInt(s[1]))

    def numberGen(l):
        s = l.split(",")
        for e in s:
            # print(e)
            yield int(e)


    cache = {}
    def inSomeRange(i):
        if i in cache:
            return cache[i]

        for k in fields:
            for r in fields[k]:
                if i <= r[1] and i >= r[0]:
                    cache[i] = True
                    return True
        
        cache[i] = False
        return False

    validNearby = []

    errorRate = 0
    for near in nearby:
        isValid = True
        for f in numberGen(near):
            if not inSomeRange(f):
                errorRate += f
                isValid = False
                break
        if isValid:
            validNearby.append(near)

    Part_1_Answer = errorRate

    assert(Part_1_Answer != 4712)

    # part 2

    # number ticket fields

    keys = list(fields.keys())
    keys.sort()
    mapping = range(len(keys))

    assert(len(keys) == sum(map( lambda x: 1, numberGen(myticket))))


    # build a nasty list:
    allFields = []
    for near in validNearby:
        thisone = []
        for i in numberGen(near):
            thisone.append(i)
        allFields.append(thisone)

    def getAllValuesInColumn(colNo):
        for ii in allFields:
            yield ii[colNo]

    def isNameOKForColumn(k, colNo):
        rSet = fields[k]
        for v in getAllValuesInColumn(colNo):
            ok = False
            for r in rSet:
                if ( v >= r[0] and v <= r[1]):
                    ok = True
            if ok is False:
                return False
        return True

    def getAllNamesForColumn(colNo):
        l = []
        for k in fields:
            if isNameOKForColumn(k, colNo):
                l.append(k)
        return l

    colNameMapping = {}
    for i in range(len(allFields[0])):
        colNameMapping[i] = getAllNamesForColumn(i)

    class breakContinue(Exception):
        pass
    # something
    
    knownNameMappings = {}
    needednames = [f for f in fields if f.find("departure") == 0]

    while len(needednames) != 0:
        l = list(map(len, colNameMapping.values()))
        #print(f"Number Name Possible: {l}")
        if 1 in l:
            i = l.index(1)
            n = colNameMapping[i][0]

            if n in needednames:
                needednames.remove(n)
            
            knownNameMappings[n] = i

            for k in colNameMapping:
                if n in colNameMapping[k]:
                    colNameMapping[k].remove(n)

            print(f"MAPPED: {n}")
        else:
            print("Stummped")
            raise RuntimeError()
    
    needednames = [f for f in fields if f.find("departure") == 0]
    myNumbers = list(numberGen(myticket))

    myAns = 1

    for n in needednames:
        m = knownNameMappings[n]
        v = myNumbers[m]
        myAns *= v

    Part_2_Answer = myAns


    return (Part_1_Answer, Part_2_Answer)

    # print(colNameMapping)
    for p in itertools.product(*(list(colNameMapping.values()))):
        s = set()
        try:
            for e in p:
                if e in s:
                    raise breakContinue()
                s.add(e)
            print("MATCH")
        except breakContinue:
            continue



    return (Part_1_Answer, Part_2_Answer)
    def generateAllColumnsSet(r=0):
        if r >= len(allFields[0]):
            return []
        for thisValue in colNameMapping[r]:
            for partial in generateAllColumnsSet(r+1):
                if thisValue in partial:
                    continue
                else:
                    p = deepcopy(partial)
                    p.append(thisValue)
                    yield p


   

    for p in generateAllColumnsSet():
        print(p)
    return (Part_1_Answer, Part_2_Answer)

    colMapCache = {}
    def isColumnMappingOk(colNo, mapNo) -> bool:
        c = (colNo, mapNo)
        if c in colMapCache:
            return colMapCache[c]

        k = keys[mapNo]

        for ii in allFields:
            i = ii[colNo]
            for r in fields[k]:
                if i <= r[1] and i >= r[0]:
                    continue
                else:
                    colMapCache[c] = False
                    return False

        colMapCache[c] = True
        return True

    for p in itertools.permutations(mapping):
        allGood = True
        for i in range(len(p)):
            if not isColumnMappingOk(i, p[i]):
                allGood = False
                break
        if allGood:
            print("OK MAPPING")

    return (Part_1_Answer, Part_2_Answer)