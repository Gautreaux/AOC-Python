import math


def dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def getAsteroidsOnRay(sightRay, pointXY, worldMap):
    width = len(worldMap[0])
    height = len(worldMap)

    def getYFromX(x):
        try:
            return (sightRay[1]/sightRay[0])*(x-pointXY[0])+pointXY[1]
        except ZeroDivisionError:
            return float('inf')

    yReturn = []
    for x in range(width):
        yTemp = getYFromX(x)
        #TODO - can do this check with an exception and catch


        if(yTemp != float('inf')):
            try:
                if(int(yTemp) != yTemp):
                    raise TypeError
                yTemp = int(yTemp)
                if(worldMap[yTemp][x] == '#'):
                    #add this asteroid to the list
                    yReturn.append((x,yTemp))
            except TypeError:
                pass
            except IndexError:
                pass
        else:
            #y is a vertical line
            for y in range(height):
                yReturn.append((x,y))
    return yReturn


def canSee(stationXY, asteroidXY, worldMap):
    #the vector from the station to the asteroid
    sightRay = (asteroidXY[0]-stationXY[0], asteroidXY[1]-stationXY[1])

    w = getAsteroidsOnRay(sightRay, stationXY, worldMap)
    
    minDist = float('inf')
    minPair = None
    for a in w:
        d = dist(a, stationXY)
        if d == 0:
            continue
        elif d < minDist:
            minDist = d
            minPair = a
    return minPair == asteroidXY

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

        for y in range(len(lineList)):
            for x in range(len(lineList[0])):
                # print(lineList[y][x], end="")
                if(lineList[y][x] == '.'):
                    continue
                k = getSightCount(lineList, x ,y)
                if(k > bestCount):
                    bestCount = k
                    bestXY = (x, y)

            print("Advancing to line " + str(y))
            # print("")

        print("The best location " + str(bestXY) + " can see " + str(bestCount));

    print("===========")

    #285 incorrect