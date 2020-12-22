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
        newTile.append("".join(reversed(row)))
    return newTile

def flipHorizontalTile(tile : TILE_TYPE) -> TILE_TYPE:
    return list(reversed(tile))

def rotateCWTile(tile : TILE_TYPE) -> TILE_TYPE:
    newTile = []
    for k in zip(*tile):
        newTile.append("".join(reversed(k)))
    return newTile

def rotateCCWTile(tile : TILE_TYPE) -> TILE_TYPE:
    """Try not to use"""
    return rotateCWTile(rotateCWTile(rotateCWTile(tile)))

def printTile(tile : TILE_TYPE, tileNum : int = None) -> None:
    if tileNum != None:
        print(f"Tile {tileNum}:")
    for r in tile:
        print("".join(r))

def getAllTileSinglePermutationsGenerator(inTile : TILE_TYPE) -> Generator[TILE_TYPE, None, None]:
    t = rotateCWTile(inTile)
    yield t
    t = rotateCWTile(inTile)
    yield t
    t = rotateCWTile(inTile)
    yield t
    yield flipHorizontalTile(inTile)
    yield flipVerticalTile(inTile)

def getAllPermutationsOfTile(tile: TILE_TYPE) -> List[TILE_TYPE]:
    tileList = [tile]
    expansionTiles = [tile]

    # # this is super overkill
    # #   should only need a handful of carefully chosen sub rotations
    # #   but NOOOOOOOO, I cant make that work
    # #   so now here we go with all the tiles

    y = 0
    while y < len(expansionTiles):
        thisTile = expansionTiles[y]
        y += 1

        for newTile in getAllTileSinglePermutationsGenerator(thisTile):
            if newTile not in tileList:
                tileList.append(newTile)
                expansionTiles.append(newTile)

    # debug checking
    for tile in tileList:
        assert(type(tile) == list)
        for row in tile:
            assert(type(row) == str)
    return tileList

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

SEA_MONSTER = [ "                  # ",
                "#    ##    ##    ###",
                " #  #  #  #  #  #   ",]
SEA_MONSTER_CHAR = "#"

POSITION_TYPE = Tuple[int, int]

def seaMonsterPositionsGenerator(s=SEA_MONSTER) -> Generator[POSITION_TYPE, None, None]:
    for y in range(len(s)):
        for x in range(len(s[y])):
            if s[y][x] == SEA_MONSTER_CHAR:
                yield ((x,y))

def isSeaMonsterAtPosition(pos : POSITION_TYPE, tile : TILE_TYPE, positionsList : List[POSITION_TYPE]) -> bool:
    for x,y in positionsList:
        if tile[pos[1] + y][pos[0] + x] != SEA_MONSTER_CHAR:
            return False
    return True

def getAllSeaMonsterPositionsGenerator(tile : TILE_TYPE):
    seaMonsterPositions = list(seaMonsterPositionsGenerator())

    for y in range(len(tile)):
        for x in range(len(tile[0])):
            try:
                if isSeaMonsterAtPosition((x,y), tile, seaMonsterPositions):
                    yield (x,y)
            except IndexError:
                pass

def getAllSeaMonsterSubPositionsGenerator(tile : TILE_TYPE):
    seaMonsterPositions = list(seaMonsterPositionsGenerator())
    for pos in getAllSeaMonsterPositionsGenerator(tile):
        for k in seaMonsterPositions:
            yield (pos[0] + k[0], pos[1] + k[1])

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
    placedTilesNumber = {}
    tilesToPlace = set(tileDict.keys())

    # generate all the tile permutations
    for tileNum in tileDict:
        assert(len(tileDict[tileNum]) == 1)
        tileDict[tileNum] = getAllPermutationsOfTile(tileDict[tileNum][0])

    # debug check
    for tileNum in tileDict:
        for tile in tileDict[tileNum]:
            for row in tile:
                assert(type(row) == str)


    thisTile = next(iter(tilesToPlace))
    tilesToPlace.remove(thisTile)
    placedTiles[(0,0)] = tileDict[thisTile][0]
    placedTilesNumber[(0,0)] = thisTile

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
                    placedTilesNumber[newPos] = matchedNum
                    
                    # update expansion edges
                    for s in SIDES:
                        nPos = getPosFromDir(newPos, s)
                        if nPos not in placedTiles:
                            expansionEdges.add((newPos, s))

                    if len(placedTiles) % 10 == 0:
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

    minX = min(map(lambda x: x[0], placedTiles))
    maxX = max(map(lambda x: x[0], placedTiles))
    minY = min(map(lambda x: x[1], placedTiles))
    maxY = max(map(lambda x: x[1], placedTiles))

    # assert that the built graph is densly packed
    for testX in range(minX, maxX+1):
        for testY in range(minY, maxY+1):
            assert((testX, testY) in placedTiles)
            assert((testX, testY) in placedTilesNumber)

    def cornersGenerator():
        yield (minX, minY)
        yield (minX, maxY)
        yield (maxX, minY)
        yield (maxX, maxY)

    Part_1_Answer = 1
    for p in cornersGenerator():
        tileNum = placedTilesNumber[p]
        Part_1_Answer *= tileNum

    print(f"Part 1 resolved to {Part_1_Answer}")

    # TODO - this should auto calculate
    tileDims = 10

    # time to collapse int one giant grid
    megaTile = []
    for y in range(maxY, minY-1, -1):
        rows = {}
        
        # initalize with empty rows
        for yy in range(tileDims):
            rows[yy] = []
        
        for x in range(minX, maxX+1):
            thisTile = placedTiles[(x,y)]
            assert(len(thisTile)) == tileDims
            for ri in range(tileDims):
                rows[ri].append(thisTile[ri])
        
        for yy in range(tileDims):
            megaTile.append("".join(rows[yy]))

    # debugMegaTile = [   ".#.#..#.##...#.##..#####",
    #                     "###....#.#....#..#......",
    #                     "##.##.###.#.#..######...",
    #                     "###.#####...#.#####.#..#",
    #                     "##.#....#.##.####...#.##",
    #                     "...########.#....#####.#",
    #                     "....#..#...##..#.#.###..",
    #                     ".####...#..#.....#......",
    #                     "#..#.##..#..###.#.##....",
    #                     "#.####..#.####.#.#.###..",
    #                     "###.#.#...#.######.#..##",
    #                     "#.####....##..########.#",
    #                     "##..##.#...#...#.#.#.#..",
    #                     "...#..#..#.#.##..###.###",
    #                     ".#.#....#.##.#...###.##.",
    #                     "###.#...#..#.##.######..",
    #                     ".#.#.###.##.##.#..#.##..",
    #                     ".####.###.#...###.#..#.#",
    #                     "..#.#..#..#.#.#.####.###",
    #                     "#..####...#.#.#.###.###.",
    #                     "#####..#####...###....##",
    #                     "#.##..#..#...#..####...#",
    #                     ".#.###..##..##..####.##.",
    #                     "...###...##...#...#..###"
    #                 ]

    # debugMonstersOrientation = rotateCWTile(flipHorizontalTile(debugMegaTile))
    # debugOrientations = list(getAllPermutationsOfTile(debugMegaTile))
    # assert(debugMonstersOrientation in debugOrientations)

    # megaTile = debugMegaTile

    results = []
    for tilePermutation in getAllPermutationsOfTile(megaTile):
        # build a mask to check which ones are in a sea monster
        m = []
        for i in range(len(tilePermutation)):
            r = []
            for ii in range(len(tilePermutation[i])):
                r.append(0)
            m.append(r)

        # seaMonsterOffsets = seaMonsterPositionsGenerator()
        # TODO - LEGACY DEBUG - remove
        seaMonsterPositions = list(getAllSeaMonsterPositionsGenerator(tilePermutation))
        print(seaMonsterPositions)

        # compute the mask
        for x,y in getAllSeaMonsterSubPositionsGenerator(tilePermutation):
            m[y][x] = 1

        # now compute the score
        score = 0
        for y in range(len(m)):
            for x in range(len(m[0])):
                if m[y][x] == 1:
                    assert(tilePermutation[y][x] == '#')
                else:
                    assert(m[y][x] == 0)
                    if tilePermutation[y][x] == '#':
                        score += 1
        results.append(score)

    print(results)
    s = set(results)
    assert(len(s) == 2)
    Part_2_Answer = min(s)


    return (Part_1_Answer, Part_2_Answer)