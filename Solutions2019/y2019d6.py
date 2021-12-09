import math

def computeDepth(planet, planetList):
    parent = planetList[planet]["Parent"]

    if(planetList[parent]["Depth"] == None):
        computeDepth(parent, planetList)
    
    planetList[planet]["Depth"] = planetList[parent]["Depth"]+1

def computeDist(planet, planetList):
    parent = planetList[planet]["Parent"]


    if(parent != None and planetList[parent]["Dist"] != None):
        t = planetList[parent]["Dist"]
        planetList[planet]["Dist"] = t+1
        return t+1

    for child in planetList[planet]["Children"]:
        if(planetList[child]["Dist"] != None):
            t = planetList[child]["Dist"]
            planetList[planet]["Dist"] = t+1
            return t+1
    
    return None

def getNeighbors(planet, planetList):
    retL = []

    parent = planetList[planet]["Parent"]
    if(parent != None):
        retL.append(parent)

    for child in planetList[planet]["Children"]:
        if(child != None):
            retL.append(child)
    
    return retL

def y2019d6(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d6.txt"
    print("2019 day 6:")

    relationList = []
    with open(inputPath) as f:
        for line in f:
            relationList.append(line.strip())

    planetList = {}
    
    for planet in relationList:
        orbited = planet[0:planet.find(")")] #the guy inside
        orbiting = planet[planet.find(")")+1:] #the guy outside

        if(orbited not in planetList):
            tempPlanet = {"Parent":None, "Children":[orbiting], "Depth":None, "Dist":None}
            planetList[orbited] = tempPlanet
        else:
            planetList[orbited]["Children"].append(orbiting)

        if(orbiting not in planetList):
            tempPlanet = {"Parent":orbited, "Children":[], "Depth":None, "Dist":None}
            planetList[orbiting] = tempPlanet
        else:
            k = planetList[orbiting]["Parent"]
            if(k != None):
                raise ValueError("Parent reassignment")
            else:
                planetList[orbiting]["Parent"] = orbited

    planetList["COM"]["Depth"] = 0

    totalDepth = 0

    for planet in planetList:
        if(planetList[planet]["Depth"] == None):
            computeDepth(planet, planetList)
        
        totalDepth += planetList[planet]["Depth"]

    print("Part 1: ", end="")
    print(totalDepth)


    #part 2
    #reset the search
    for planet in planetList:
        planetList[planet]["Dist"] = None
    
    planetList["YOU"]["Dist"] = 0

    nList = getNeighbors("YOU", planetList)
    searchQ = []
    for e in nList:
        planetList[e]["Dist"] = 1
        searchQ.append(e)
    
    while(len(searchQ) != 0):
        myP = searchQ[0]
        searchQ = searchQ[1:]
    
        if(myP == None):
            continue
        else:
            # computeDist(myP, planetList)
            nList = getNeighbors(myP, planetList)
            for e in nList:
                if(planetList[e]["Dist"] == None):
                    planetList[e]["Dist"] = planetList[myP]["Dist"]+1
                    searchQ.append(e)

    print(planetList["SAN"]["Dist"]-2)
    print("===========")

    return(totalDepth, planetList["SAN"]["Dist"]-2)

    #part 2 - 462 is wrong
    #367 is wrong