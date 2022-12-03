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

# ==================

from collections import deque
from dataclasses import dataclass, field
from typing import Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T


@dataclass
class Planet:
    """A Planet"""

    name: str
    
    orbiting: Optional['Planet'] = None

    moons: set['Planet'] = field(default_factory=set)

    _depth: int = field(default=-1, init=False, compare=False, hash=False)

    @property
    def depth(self) -> int:
        """The distance (orbital transfers) from `COM`. Also Number Orbits"""
        if self._depth == -1:
            self._depth = self.orbiting.depth + 1 
        return self._depth

    def __hash__(self) -> int:
        return hash(self.name)


class Solution_2019_06(SolutionBase):
    """https://adventofcode.com/2019/day/6"""

    def _get_planet(self, name: str) -> Planet:
        try:
            return self.planets[name]
        except KeyError:
            p = Planet(name)
            self.planets[name] = p
            return p

    def __post_init__(self):
        """Runs Once After `__init__`"""
        
        self.planets: dict[str, Planet] = {}

        for r in self.input_str_list():
            base, _, moon = r.partition(')')  

            base_planet = self._get_planet(base)
            moon_planet = self._get_planet(moon)

            base_planet.moons.add(moon_planet)
            if moon_planet.orbiting is not None:
                raise RuntimeError
            else:
                moon_planet.orbiting = base_planet

        self.planets['COM']._depth = 0


    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        return sum(map(
            lambda p: p.depth,
            self.planets.values(),
        ))

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        target = self.planets['SAN'].orbiting

        visited = set()
        frontier: deque[tuple[Planet, int]] = deque()
        frontier.append((self.planets['YOU'], 0))

        while frontier:
            (new_p, new_d) = frontier.popleft()

            if new_p.name == target.name:
                return new_d

            visited.add(new_p.name)

            if new_p.orbiting is not None and new_p.orbiting.name not in visited:
                frontier.append((new_p.orbiting, new_d + 1))
            
            for m in new_p.moons:
                if m.name not in visited:
                    frontier.append((m, new_d + 1))
