import math


def dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def getRay(p1, p2):
    return ((p2[0]-p1[0]),(p2[1]-p1[1]))


def canSee(stationXY, asteroidXY, worldMap):
    #the vector from the station to the asteroid
    sightRay = getRay(stationXY, asteroidXY)
    minDist = dist(stationXY, asteroidXY)
    
    for y in range(len(worldMap)):
        for x in range(len(worldMap[0])):
            if((x,y) == stationXY):
                continue
            if((x,y) == asteroidXY):
                continue
            if(dist(stationXY, (x,y)) < minDist and getRay(stationXY, (x,y)) == sightRay):
                return False

def getSightCount(lineList, xStat, yStat):
    'return the number of asteroids visible from this point'
    sightCount = 0
    for y in range(len(lineList)):
        for x in range(len(lineList[0])):
            if(xStat == x and yStat == y):
                #skip the same
                continue
            elif(lineList[y][x] == '.'):
                #skip empties
                continue
            elif(canSee((xStat,yStat), (x,y), lineList)):
                #can this point see the station?
                sightCount+=1
    return sightCount

def y2019d10(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d10.txt"
    print("2019 day 10:")

    with open(inputPath) as f:
        lineList = []
        for line in f:
            #do something
            lineList.append(line.strip())
        

        # print(len(lineList))

        bestXY = (None, None)
        bestCount = 0

        asteroidPos = [] # a list of all the asteroids

        for y in range(len(lineList)):
            for x in range(len(lineList[0])):
                asteroidPos.append((x,y))

        for y in range(len(lineList)):
            for x in range(len(lineList[0])):
                # print(lineList[y][x], end="")
                if(lineList[y][x] == '.'):
                    continue
                k = getSightCount(lineList, x ,y)
                if(k > bestCount):
                    bestCount = k
                    bestXY = (x, y)

            print("Advancing to line " + str(y+1))
            # print("")

        print("The best location " + str(bestXY) + " can see " + str(bestCount));

    print("===========")

    #285 incorrect