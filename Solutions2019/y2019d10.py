import math

def hashPair(tuple1):
    return tuple1[0]*20+tuple1[1]

def getDist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def getRay(p1, p2):
    r =  ((p2[0]-p1[0]),(p2[1]-p1[1]))
    rmag = getDist(r, (0,0))
    return (round(r[0]/rmag,6), round(r[1]/rmag,6))

def findStandardFormAngularDistance(station, asteroid):
    #get the angle between the station and the asteroid in radians
    #in standard form i might add
    ray = getRay(station, asteroid)
    ang = math.atan2(ray[1], ray[0])
    if(ang < 0):
        ang += math.pi*2
    return ang

def findAngularDistance(station, laserOrientation, asteroid):
    #laser orientation is already in [0, 2pi)
    
    astStandDist = findStandardFormAngularDistance(station, asteroid)
    if(astStandDist == laserOrientation):
        return 0
    if(laserOrientation > astStandDist):
        return laserOrientation - astStandDist
    if(laserOrientation < astStandDist):
        return 2*math.pi-astStandDist+laserOrientation
    raise ValueError("How did you get here?")
    

def vaporize(asteroidList, laserOrientation, station):
    #laser orientation should be in range [0,2pi)
    #find the closest asteroid to vaporize 

    minAngDist = 2*math.pi
    linearDist = float("inf")
    minAst = None

    for asteroid in asteroidList:
        if(asteroid == station):
            continue
        angDist = findAngularDistance(station, laserOrientation, asteroid)
        linDist = getDist(station, asteroid)
        if(angDist < minAngDist):
            minAngDist = angDist
            linearDist = linDist
            minAst = asteroid
        elif(angDist == minAngDist and linDist < linearDist):
            linearDist = linDist
            minAst = asteroid
    
    if(minAngDist < 0):
        print("Found negative angular distance: " + str(minAngDist) + " on " + str(minAst))
    return (minAngDist, minAst)

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

        print("PART 1:The best location " + str(bestXY) + " can see " + str(bestCount));

        laserOrientation = math.pi/2 #90deg in radians (up on the standard repr)
        #rotates clockwise

        asteroidPosCopy = asteroidPos #store a copy of the original asteroid list

        stationLocation = bestXY

        #recenter the list have station at 0,0
        fixedAsteroidList = []
        for asteroid in asteroidPos:
            fixedAsteroidList.append((asteroid[0]-stationLocation[0],asteroid[1]-stationLocation[1]))

        #modify so that positive y is the up direction
        asteroidPos = []
        for fAsteroid in fixedAsteroidList:
            asteroidPos.append((fAsteroid[0], -fAsteroid[1]))


        #items destroyed
        destorycounter = 0

        for i in range(1,201):
            (aDist, asteroid) = vaporize(asteroidPos, laserOrientation, (0,0))

            origAsteroid = asteroidPosCopy[asteroidPos.index(asteroid)]

            if(i == 200):
                break

            # print("["+str(i)+"] " + str(asteroid) + " " + str(origAsteroid))
            asteroidPos.remove(asteroid)
            asteroidPosCopy.remove(origAsteroid)
            
            if(aDist == 0 and not(i == 1)):
                print("Warning: no laser motion between destroys: " + str(i))
            laserOrientation -= aDist
            laserOrientation -= .0000001 #make move for the next one
            if(laserOrientation < 0):
                laserOrientation+=2*math.pi

            # destorycounter+=1
            # print("Destroyed " + str(destorycounter))

            
        # (aDist, asteroid) = vaporize(asteroidPos, laserOrientation, (0,))
        origAsteroid = asteroidPosCopy[asteroidPos.index(asteroid)]
        print("The 200th (part 2) asteroid to be destroyed is " + str(origAsteroid) + ". part2 value: " + str(origAsteroid[0]*100+origAsteroid[1]))

    print("===========")

    #285 incorrect
    #728 too high
    #404 too high
    #295 incorrect

    #part 2
    #1413 too high
    #1213 too high

    return(bestCount, str(origAsteroid[0]*100+origAsteroid[1]))
