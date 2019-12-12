

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

    lPos = None
    lVel = None

    print(planetList)
    print(velocityList)
    print("========0")

    for i in range(1000):
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

    totalEnergy = 0
    for i in range(4):
        pE = 0
        kE = 0
        for axis in range(3):
            pE+= abs(planetList[i][axis])
            kE += abs(velocityList[i][axis])

        totalEnergy+= pE*kE
    
    print(str(totalEnergy))

    print("===========")


    #74074531000 too high