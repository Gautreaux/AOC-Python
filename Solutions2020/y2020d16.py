# from AOC_Lib.name import *
import itertools
from copy import deepcopy


def y2020d16(inputPath=None):
    if inputPath == None:
        inputPath = "Input2020/d16.txt"
    print("2020 day 16:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    type1Lines = []  # all lines that are defining names
    myTicket = None  # the line of my ticket
    nearby = []  # the lines in the nearby category

    for l in lineList:

        if l in ["", "your ticket:", "nearby tickets:"]:
            continue
        i = l.find("or")
        if i != -1:
            type1Lines.append(l)
        else:
            if myTicket is None:
                myTicket = l
            else:
                nearby.append(l)

    # print(type1Lies)
    # print(myTicket, end = "\n\n\n\n\n\n")
    # print(nearby)

    fields = {}

    def splitInt(s):
        """Split the range into its int componenets"""
        s = s.strip()
        k = s.split("-")
        return (int(k[0]), int(k[1]))

    for c in type1Lines:
        # split the title lines for their components
        s = c.split(":")
        name = s[0]
        s = s[1].strip().split(" or ")
        fields[name] = (splitInt(s[0]), splitInt(s[1]))

    def numberGen(l):
        """Generate all the numbers for the given line"""
        s = l.split(",")
        for e in s:
            # print(e)
            yield int(e)

    cache = {}

    def inSomeRange(i):
        """Return True if i is in any of the ranges. Cached."""
        if i in cache:
            return cache[i]

        for k in fields:
            for r in fields[k]:
                if i <= r[1] and i >= r[0]:
                    cache[i] = True
                    return True

        cache[i] = False
        return False

    validNearby = []  # the tickets that are in nearby and valid
    errorRate = 0

    # part 1 - caluclating the error rate
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

    assert Part_1_Answer != 4712

    # part 2

    # number ticket fields

    keys = list(fields.keys())
    keys.sort()
    mapping = range(len(keys))

    assert len(keys) == sum(map(lambda x: 1, numberGen(myTicket)))

    # repack the nearby numbers into a 2d array
    allFields = []
    for near in validNearby:
        thisone = []
        for i in numberGen(near):
            thisone.append(i)
        allFields.append(thisone)

    def getAllValuesInColumn(colNo):
        """ "Generator for all values in a given column"""
        for ii in allFields:
            yield ii[colNo]

    def isNameOKForColumn(colName, colNo):
        """ "Return true iff the name is acceptable for the number"""
        rSet = fields[colName]
        for v in getAllValuesInColumn(colNo):
            ok = False
            for r in rSet:
                if v >= r[0] and v <= r[1]:
                    ok = True
            if ok is False:
                return False
        return True

    def getAllNamesForColumn(colNo):
        """Generator for all the names for the given column number"""
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

    # something - to break up the linter

    knownNameMappings = {}  # mapping of know names to columns

    # the names needed before part two can be answered
    needednames = [f for f in fields if f.find("departure") == 0]

    while len(needednames) != 0:
        l = list(map(len, colNameMapping.values()))
        # print(f"Number Name Possible: {l}")
        if 1 in l:
            # the obvious mapping can be completed
            i = l.index(1)
            n = colNameMapping[i][0]

            if n in needednames:
                needednames.remove(n)

            knownNameMappings[n] = i

            for k in colNameMapping:
                if n in colNameMapping[k]:
                    colNameMapping[k].remove(n)

            # print(f"MAPPED: {n}")
        else:
            print("IDK what to do now that no obvious choice exists")
            print("Probably do an all pairs generation?")
            raise RuntimeError()

    needednames = [f for f in fields if f.find("departure") == 0]
    myNumbers = list(numberGen(myTicket))

    # getting ready for part 2
    myAns = 1
    for n in needednames:
        m = knownNameMappings[n]
        v = myNumbers[m]
        myAns *= v

    Part_2_Answer = myAns

    return (Part_1_Answer, Part_2_Answer)
