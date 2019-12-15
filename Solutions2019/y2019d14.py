import math

from AOC_Lib.queue import Queue

#TODO - modify this code to accept exactly one producing reaction

class Element():
    def __init__(self, nameStr):
        self.producingReactions = [] #list of reactions where this element is produced
        self.consumingReactions = [] #list of reactions where this element is consumed
        self.name = nameStr

def getPairs(strIn):
    #returns a list of pairs that form the input 
    returnList = []

    while(len(strIn) > 3):
        c = strIn.find(" ")
        c2 = strIn.find(" ", c+1)

        v = strIn[c+1:c2]
        if(v[len(v)-1] == ','):
            v = v[:len(v)-1]

        returnList.append((int(strIn[0:c]), v))

        strIn = strIn[c2+1:]
    
    return returnList

def y2019d14(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d14.txt"
    print("2019 day 14:")

    with open(inputPath) as f:
        relations = [] #list of all relations
        elementsDict = {} #pointer to the elements objects
        for line in f:
            break1 = line.find("=>")
            inputs = line[:break1] + " "
            outputs = line[break1+3:].strip()+"  "

            inputList = getPairs(inputs)
            outputList = getPairs(outputs)

            rel = (inputList, outputList)
            relations.append(rel)

            for r in inputList:
                n = r[1]
                if(n not in elementsDict):
                    elementsDict[n] = Element(n)
                
                e = elementsDict[n]
                e.consumingReactions.append(rel)
            
            for r in outputList:
                n = r[1]
                if(n not in elementsDict):
                    elementsDict[n] = Element(n)
                
                e = elementsDict[n]
                e.producingReactions.append(rel)

            
        for key in elementsDict:
            e = elementsDict[key]
            k = len(e.producingReactions)
            if(k == 0):
                if(e.name != "ORE"):
                    print("Element " + str(e.name) + " does not have a producing reaction.")
                    return
            elif(k != 1):
                print("Element " + str(name) + " has " + str(k) + " producing reactions.")

        for rel in relations:
            if(len(rel[1]) > 1):
                print("Warning: multiple product production found.")

        print("Passed producing check.")
        #now this has gotten pretty easy

        requirementsDict = {}

        for k in elementsDict:
            requirementsDict[k] = 0

        requirementsQ = Queue()
        requirementsQ.pushBack("FUEL")
        requirementsDict["FUEL"] = 1

        while(len(requirementsQ) > 0):
            thisReq = requirementsQ.pop() #the name of the item we need to produce

            if(thisReq == "ORE"):
                break

            thisElement = elementsDict[thisReq] #the element
            thisRel = thisElement.producingReactions[0] #the producing relation
            thisCount = requirementsDict[thisReq] #the total quantity to produce
            thisReactionsRequired = thisCount/(thisRel[1][0][0])

            if(thisReactionsRequired != int(thisReactionsRequired)):
                thisReactionsRequired = math.ceil(thisReactionsRequired)
                # raise ValueError("The reaction needs to occur a non-integer number of times")

            #loop over the reaction inputs
            for e in thisRel[0]:
                item = e[1]
                count = e[0]
                countCycles = count*thisReactionsRequired
                requirementsDict[item] += countCycles
                requirementsQ.pushBack(item)
        
        print("Ore Required (Part 1): " + str(requirementsDict["ORE"]))
    
    print("===========")

    #436 too low