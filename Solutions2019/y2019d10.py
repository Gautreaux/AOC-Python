import math

def hashPair(tuple1):
    return tuple1[0]*20+tuple1[1]

def getDist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def getRay(p1, p2):
    r =  ((p2[0]-p1[0]),(p2[1]-p1[1]))
    rmag = getDist(r, (0,0))
    return (round(r[0]/rmag,6), round(r[1]/rmag,6))

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
                if(lineList[y][x] == '#'):
                    asteroidPos.append((x,y))

        print(len(asteroidPos))

        for asteroid in asteroidPos:
            takenRaysDict = {} #maps a ray to a distance
            rayDict = {}

            for otherAsteroid in asteroidPos:
                if(otherAsteroid == asteroid):
                    continue
                rt = getRay(asteroid, otherAsteroid)
                r = hashPair(rt)

                if(r not in rayDict):
                    rayDict[r] = rt
                else:
                    if(rayDict[r] != rt):
                        print("HASH COLLISION:" + str(rayDict[r])+  " " + str(rt))

                d = getDist(asteroid, otherAsteroid)
                if(r not in takenRaysDict):
                    takenRaysDict[r] = d
                else:
                    if(d < takenRaysDict[r]):
                        takenRaysDict[r] = d
            
            totalVisible = len(takenRaysDict)
            if(totalVisible > bestCount):
                bestCount = totalVisible
                bestXY = asteroid

        print("The best location " + str(bestXY) + " can see " + str(bestCount));

    print("===========")

    #285 incorrect
    #728 too high
    #404 too high
    #295 incorrect