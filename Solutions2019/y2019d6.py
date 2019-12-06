import math

def computeDepth(planet, planetList):
    parent = planetList[planet]["Parent"]

    if(planetList[parent]["Depth"] == None):
        computeDepth(parent, planetList)
    
    planetList[planet]["Depth"] = planetList[parent]["Depth"]+1


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
            tempPlanet = {"Parent":None, "Children":[orbiting], "Depth":None}
            planetList[orbited] = tempPlanet
        else:
            planetList[orbited]["Children"].append(orbiting)

        if(orbiting not in planetList):
            tempPlanet = {"Parent":orbited, "Children":[], "Depth":None}
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

    print(totalDepth)


    



    print("===========")