# from AOC_Lib.name import *

from readmeFormatter import doAutoGen
from typing import Generator, List, NewType, Optional, Tuple


def constructTile(fileGen : Generator[str, None, None]) -> Tuple[int, List[str]]:
    thisTile = []
    thisNum = None
    
    for s in fileGen:
        if s == "":
            assert(thisNum != None)
            yield (thisNum, thisTile)
            thisNum = None
            thisTile = []
            continue
        i = s.find("Tile")
        if i == -1:
            thisTile.append(s)
        else:
            assert(thisNum == None)
            assert(thisTile == [])
            thisNum = int(s.replace(":", "").split(" ")[1])



Side_TYPE = int
TILE_TYPE = List[str]
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
SIDES = [UP, RIGHT, DOWN, LEFT]

def getOppositeSide(side : Side_TYPE) -> Side_TYPE:
    return (side + 2) % 4

def getTileSideIterator(tile : TILE_TYPE, side : Side_TYPE) -> Generator[str,None, None]:
    assert(side in SIDES)

    if side == UP:
        for i in tile[0]:
            yield i
    elif side == DOWN:
        for i in tile[-1]:
            yield i
    elif side == LEFT:
        for i in tile:
            yield i[0]
    elif side == RIGHT:
        for i in tile:
            yield i[-1]

def doesEdgeAlign(knownTile : TILE_TYPE, matchTile : TILE_TYPE, side :Side_TYPE) -> bool:
    """Check if match tile first on side of knownTile"""

    # side is the side on the known tile
    knownGen = getTileSideIterator(knownTile, side)
    # need to opposite side for the match tile
    matchGen = getTileSideIterator(matchTile, getOppositeSide(side))

    while True:
        try:
            k = next(knownGen)
        except StopIteration:
            try:
                # we expect this to throw stop iteration
                n = next(matchGen)
            except StopIteration:
                # both generators ended at the same time
                return True
            # the known generator stopped first
            # (generators different lengths)
            return False
        
        try:
            n = next(matchGen)
        except StopIteration:
            # the match generator stopped before the known generator
            return False
        if k != n:
            return False
    # should be unreachable, but everything matched
    return True


def flipVerticalTile(tile : TILE_TYPE) -> TILE_TYPE:
    # flip over the vertical axis
    newTile = []
    for row in tile:
        newTile.append(list(reversed(row)))
    return newTile

def flipHorizontalTile(tile : TILE_TYPE) -> TILE_TYPE:
    return list(reversed(tile))

def rotateCWTile(tile : TILE_TYPE) -> TILE_TYPE:
    newTile = []
    for k in zip(*tile):
        newTile.append(list(reversed(k)))
    return newTile

def rotateCCWTile(tile : TILE_TYPE) -> TILE_TYPE:
    """Try not to use"""
    return rotateCWTile(rotateCWTile(rotateCWTile(tile)))

def printTile(tile : TILE_TYPE, tileNum : int = None) -> None:
    if tileNum != None:
        print(f"Tile {tileNum}:")
    for r in tile:
        print("".join(r))

def getAllTileSinglePermutationsGenerator(inTile):
    t = rotateCWTile(inTile)
    yield t
    t = rotateCWTile(inTile)
    yield t
    t = rotateCWTile(inTile)
    yield t
    yield flipHorizontalTile(inTile)
    yield flipVerticalTile(inTile)

def getPosFromDir(position : Tuple[int, int], side : Side_TYPE) -> Tuple[int, int]:
    x = position[0]
    y = position[1]
    if side == LEFT:
        return (x-1, y)
    elif side == UP:
        return (x, y+1)
    elif side == DOWN:
        return (x, y-1)
    elif side == RIGHT:
        return (x+1, y)
    else:
        raise ValueError(side)

def y2020d20(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2020/d20.txt"
    print("2020 day 20:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    tileDict = {}

    for tileNum, tile in constructTile(iter(lineList)):
        tileDict[tileNum] = [tile]

    print(f"Total Tiles: {len(tileDict)}")

    # debug
    # debugTile = [["A", "B", "C"], ["D", "E", "F"], ["H", "I", "J"]]
    # printTile(debugTile, -1)
    # printTile(rotateCWTile(debugTile), -1)

    placedTiles = {}
    tilesToPlace = set(tileDict.keys())

    # generate all the tile permutations
    for tileNum in tileDict:
        l : List[TILE_TYPE] = tileDict[tileNum]

        # this is super overkill
        #   should only need a handful of carefully chosen sub rotations
        #   but NOOOOOOOO, I cant make that work
        #   so now here we go with all the tiles
        expansionTiles = [l[0]]
        i = 0   
        
        while i < len(expansionTiles):
            thisTile = expansionTiles[i]
            i += 1

            for newTile in getAllTileSinglePermutationsGenerator(thisTile):
                if newTile not in l:
                    l.append(newTile)
                    expansionTiles.append(newTile)


    thisTile = next(iter(tilesToPlace))
    tilesToPlace.remove(thisTile)
    placedTiles[(0,0)] = tileDict[thisTile][0]

    expansionEdges = set()
    expansionEdges.add(((0,0), LEFT))
    expansionEdges.add(((0,0), UP))
    expansionEdges.add(((0,0), DOWN))
    expansionEdges.add(((0,0), RIGHT))

    class BreakContinue(Exception):
        pass

    while len(tilesToPlace) != 0:
        try:
            for expansionCandidate in expansionEdges:
                rootPos = expansionCandidate[0]
                expandDirection = expansionCandidate[1]
                candidates = []

                newPos = getPosFromDir(rootPos, expandDirection)
                if newPos in placedTiles:
                    expansionEdges.remove(expansionCandidate)
                    raise BreakContinue

                for tileNum in tilesToPlace:
                    for tile in tileDict[tileNum]:
                        if doesEdgeAlign(placedTiles[rootPos], tile, expandDirection):
                            candidates.append((tileNum, tile))
                if len(candidates) == 0:
                    # print("NO MATCH POSSIBLE")
                    pass
                elif len(candidates) == 1:
                    matchedNum, matchTile = candidates[0]
                    # newPos = getPosFromDir(rootPos, expandDirection)
                    tilesToPlace.remove(matchedNum)
                    # print("A MATCH OCCURRED")
                    # update the placed tiles
                    placedTiles[newPos] = matchTile
                    
                    # update expansion edges
                    for s in SIDES:
                        nPos = getPosFromDir(newPos, s)
                        if nPos not in placedTiles:
                            expansionEdges.add((newPos, s))

                    print(f"{len(placedTiles)} of {len(tileDict)} tiles placed")

                    raise BreakContinue
        except BreakContinue:
            continue
        #TODO - why is one of the rotation thingies breaking into a list,
        #   and how to make it into a string
        print("Not sure what to do here")
        raise NotImplementedError()

    assert(len(tilesToPlace) == 0)
    print("All tiles successfully placed")

    # TODO - compute the actual answer
    return (Part_1_Answer, Part_2_Answer)