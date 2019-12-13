import copy

def listHash2(lIn):
    return hash((listHash4(lIn[0]), listHash4(lIn[1])))

def listHash3(lIn):
    return hash((lIn[0], lIn[1], lIn[2]))

def listHash4(lIn):
    return hash((listHash3(lIn[0]), listHash3(lIn[1]), listHash3(lIn[2]), listHash3(lIn[3])))

def otherListHash2(lIn):
    return hash((otherListHash4(lIn[0]), otherListHash4(lIn[1])))

def otherListHash4(lIn):
    return hash((lIn[0], lIn[1], lIn[2], lIn[3]))

class Planet():
    def __init__(self, positionList):
        self.position = positionList
        self.velocity = [0,0,0]
    
def y2019d12(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d2.txt"
    print("2019 day 2:")

    with open(inputPath) as f:
        for line in f:
            #TODO - actually read in
            pass

    #input
    planetList = [[3,2,-6],[-13,18,10],[-8,-1,13],[5,10,4]]

    #sample1
    # planetList = [[-1,0,2],[2,-10,-7],[4,-8,8], [3,5,-1]]


    velocityList = [[0,0,0], [0,0,0,], [0,0,0], [0,0,0]]

    stateDict = {}
    stateDictList = [{},{},{}]
    solList = [None, None, None]

    print(planetList)
    print(velocityList)
    print("========0")

    ctr = 0
    while(True):
        # break
        #simulate a time step

        #update all velocities (apply gravity)
        for i in range(4):
            for j in range(4):
                if(i == j):
                    continue

                for axis in range(3):
                    if(planetList[i][axis] > planetList[j][axis]):
                        velocityList[i][axis] -=1
                    elif(planetList[i][axis] < planetList[j][axis]):
                        velocityList[i][axis] += 1

        #update positions
        for i in range(4):
            for axis in range(3):
                planetList[i][axis] += velocityList[i][axis]

        # print(planetList)
        # print(velocityList)
        # print("========" + str(i+1))

        #for part 2:
        for dimension in range(3):
            t = [[planetList[0][dimension], planetList[1][dimension], planetList[2][dimension], planetList[3][dimension]], [velocityList[0][dimension],velocityList[1][dimension], velocityList[2][dimension], velocityList[3][dimension]]]
            tt = otherListHash2(t)
            # print(tt)
            if(tt not in stateDict):
                stateDict[tt] = [copy.deepcopy(t)]
            else:
                if(t in stateDict[tt]):
                    if(solList[dimension] == None):
                        print("Found dimension: " + str(dimension))  
                        solList[dimension] = ctr
                    else:
                        # print("DUPE FOUND")
                        pass

                else:
                    stateDict[tt].append(copy.deepcopy(t))

        if(None not in solList):
            break

        ctr+=1
        if(ctr == 1000):
            totalEnergy = 0
            for i in range(4):
                pE = 0
                kE = 0
                for axis in range(3):
                    pE+= abs(planetList[i][axis])
                    kE += abs(velocityList[i][axis])

                totalEnergy+= pE*kE
            
            print(str(totalEnergy))
        
        if(ctr%100000 == 0):
            print("Heartbeat: " + str(ctr))

        # if(ctr >= 1000000):
        #     print("Infinite loop, breaking")
        #     break

    # print("Fixed value debug")
    # solList = [186028, 84032, 286332]

    print("Found periods:"+ str(solList))

    #so we need to find the first value I where I%each of those is the same
    #but i has to be grater than the smallest
    solList.sort()
    i = solList[0]

    ctr = 0
    # #Takes forever 
    #TODO - can this be multiprocessed and eventually terminate?
    #                       it will eventually, but is it reasonablely short?
    # while(True):
    #     i = 279751820342592 %but it would have terminated
    #     t = i %solList[0]
    #     if(t == i %solList[1] and t == i %solList[2]):
    #         print("Part 2: " + str(i))
    #         break
    
    #     i+=solList[0]
    #     ctr+=1
    #     if(ctr %100000 == 0):
    #         print("Heartbeat: " + str(ctr))

    #use an online LCM calculator, you'll get:
    print("Part 2: " + str(279751820342592))


    print("===========")


    #74074531000 too high