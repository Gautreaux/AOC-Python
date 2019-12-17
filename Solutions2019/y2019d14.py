import math

from AOC_Lib.queue import Queue

#TODO - modify this code to accept exactly one producing reaction
#TODO - this problem part 2 is a network flow problem?
#       or with a topological sort

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
                print("Element " + str(e.name) + " has " + str(k) + " producing reactions.")

        productionBool = True

        #assert that each product can be produced only once 
        #this ensures that no feedback loops can exist as either
        #   the product is already in the feedback loop
        #       but how did the loop start?
        #   or this product isnt in a loop
        for e in elementsDict:
            element = elementsDict[e]
            if(len(element.producingReactions) > 1):
                print("Warning: looped production possible.")
                productionBool = False

            #this makes sure that everything is eventually used to produce fuel
            if(len(element.consumingReactions) == 0 and element.name != "FUEL"):
                print("Warning: found non-fuel terminal chain.")
                productionBool = False

        #check that each reaction has exactly one product
        for rel in relations:
            if(len(rel[1]) > 1):
                print("Warning: multiple product production found.")
                productionBool = False

            if(len(rel[1]) == 0):
                print("Warning: Found reaction with no products")
                productionBool = False
            
        if(productionBool == True):
            # print("Passed producing checks.")
            pass
        else:
            print("Failed one or more production checks.")
        #now this has gotten pretty easy


        def getOreRequirementsForFuel(reqAmount):
            requirementsDict = {} #requirements that we are trying to satisfy
            doneList = []

            for k in elementsDict:
                requirementsDict[k] = 0

            requirementsQ = Queue()
            requirementsQ.pushBack("FUEL")
            requirementsDict["FUEL"] = reqAmount

            while(len(requirementsQ) > 0):
                thisReq = requirementsQ.pop() #the name of the item we need to produce

                if(thisReq == "ORE"):
                    if(len(requirementsQ) != 0):
                        # print("Warning, the dict may have exited prematurely")
                        requirementsQ.pushBack("ORE")
                        continue
                    else:
                        break

                doneList.append(thisReq)
                

                thisElement = elementsDict[thisReq] #the element
                thisRel = thisElement.producingReactions[0] #the producing relation
                thisCount = requirementsDict[thisReq] #the total quantity to produce
                thisReactionsRequired = thisCount/(thisRel[1][0][0])

                if(thisReactionsRequired != int(thisReactionsRequired)):
                    excessProduced = round((math.ceil(thisReactionsRequired)-thisReactionsRequired)*thisRel[1][0][0],4)
                    if(excessProduced != int(excessProduced)):
                        raise Exception("Excess non-integer exception: " + str(excessProduced))
                    thisReactionsRequired = math.ceil(thisReactionsRequired)
                    # raise ValueError("The reaction needs to occur a non-integer number of times")
                    requirementsDict[thisReq] = -int(excessProduced)
                else:
                    #reset the requirements dict
                    requirementsDict[thisReq] = 0

                #loop over the reaction inputs
                for e in thisRel[0]:
                    item = e[1]
                    count = e[0]
                    countCycles = count*thisReactionsRequired

                    # if(item in doneList):
                    #     if(item == 'ORE'):
                    #         print("BIG OOF")
                    #     requirementsDict[item] = 0
                    #     doneList.remove(item)

                    requirementsDict[item] += countCycles

                    if(item not in requirementsQ):
                        requirementsQ.pushBack(item)

            return requirementsDict["ORE"]

        
        print("Ore Required (Part 1): " + str(getOreRequirementsForFuel(1)))

        maxOre = 1000000000000
        fuelCtr = 1
        fuelIncrement = 1

        while(True):
            t = getOreRequirementsForFuel(fuelCtr+fuelIncrement)
            if(t <= maxOre):
                fuelCtr+=fuelIncrement
                fuelIncrement*=2
            else:
                if(fuelIncrement == 1):
                    break
                else:
                    #reset the increment and try again
                    fuelIncrement = 1

        print("From one trillion ore (Part 2), "  + str(fuelCtr) + " fuel can be produced.")

        
    
    print("===========")

    #part 1:
    #436 too low

# if __name__ == "__main__":
#     from Solutions2019.y2019d14 import y2019d14
#     print("165, ????:")
#     y2019d14("Input2019/d14-sample.txt")
#     print("13312, 8292753:")
#     y2019d14("Input2019/d14-sample2.txt")
#     print("180697, 5586022:")
#     y2019d14("Input2019/d14-sample3.txt")
#     print("2210736, 460664:")
#     y2019d14("Input2019/d14-sample4.txt")
#     print("????, ????:")
#     y2019d14()