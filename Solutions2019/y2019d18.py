import copy
from AOC_Lib.queue import Queue
from AOC_Lib.pqueue import PQueue
from math import sqrt
import heapq

def manhattanDist(sPos, ePos):
    return sqrt((sPos[0]-ePos[0])**2+(sPos[1]-ePos[1])**2)


#TODO - this should be reworked into a general pair-bimap class
class KeyDoor():
    #the key door pair construct
    def __init__(self, key, door):
        self.k = key
        self.d = door
    
    def __eq__(self, other):
        return self.k == other.k
    
    def __lt__(self, other):
        return self.k < other.k

    def __hash__(self):
        return hash((self.k, self.d))

#this is a simple override of list for some hashing functionality
#for part 2
class PosList():
    def __init__(self, posList):
        self.p = posList
        self.p.sort()
    
    def __hash__(self):
        return hash((self.p[0],self.p[1],self.p[2],self.p[3]))
    
    def __len__(self):
        return len(self.p)
    
    def __eq__(self, other):
        return self.p == other.p

    def __getitem__(self, index):
        return self.p[index]
    
    def __setitem__(self, index, value):
        self.p[index] = value

class MazeState():
    #track the key hash values

    def __init__(self, position, keyDoorList, d = 0, doorList = None):
        self.pos = position
        self.kList = keyDoorList
        self.depth = d

        self.kList.sort()

        if(doorList == None):
            self.dList = []
            for k in self.kList:
                self.dList.append(k.d)
            self.dList.sort()
        else:
            self.dList = doorList
        

    def __kListHash(self):
        e = 0
        for key in self.kList:
            e = hash((key, e))
        return e

    def __hash__(self):
        #perform the hash operation
        return hash((hash(self.pos), self.__kListHash()))
    
    def __eq__(self, other):
        try:
            if(self.pos != other.pos):
                return False
            if(self.kList != other.kList):
                return False
            return True
        except AttributeError as A:
            if(type(other) == type(None)):
                return False 
            raise A

def getHeuristicPriority(state):
    return 1

class MazeStatePriority():
    def __init__(self, state):
        self.state = state
        self.__priority = state.getHeuristicPriority()
    
    def __lt__(self, other):
        return self.__priority < other.__priority
    
    def __eq__(self, other):
        return self.__priority == other.__priority

def generateSuccessorStates(state, wallList):
    #returns a list of valid states from the current state
    successorList = []

    transforms = [(0,1),(0,-1),(-1,0),(1,0)]

    for transform in transforms:
        newState = MazeState((0,0), state.kList, d=state.depth+1, doorList=state.dList)
        newPos = (state.pos[0]+transform[0], state.pos[1]+transform[1])

        kdPos = KeyDoor(newPos, (0,0))

        if(kdPos in state.kList):
            #need to remove the key,door pair
            kdList = copy.copy(state.kList)
            kdList.remove(KeyDoor(newPos, (0,0)))
            newState = MazeState(newPos, kdList, d=state.depth+1)
            pass
        else:
            newState.pos = newPos
        
        if(isValidState(newState, wallList)):
            successorList.append(newState)

    return successorList

def isValidState(state, wallList):
    if(state.pos in wallList):
        return False
    if(state.pos in state.dList):
        return False
    return True

def isGoalState(state):
    #returns true iff this is a goal state
    #a goal state is on in which there are no keys remaining
    return len(state.kList) == 0

#todo, refactor into the lib
def searchLoop(startState, successorGenerator, goalCheck, report=False):
    visitedHashTable = {}
    stateQ = Queue()
    stateQ.pushBack(startState)
    # stateQ = PQueue()
    # stateQ.push(startState, getHeuristicPriority(startState))
    foundGoal = None

    nextReport = 0

    while(len(stateQ) > 0):
        thisState = stateQ.pop()
        # thisState = stateQ.popMin()
        thisHash = hash(thisState)

        #check if state is already visited
        if(thisHash not in visitedHashTable):
            visitedHashTable[thisHash] = [thisState]
        else:
            if(thisState in visitedHashTable[thisHash]):
                continue
            else:
                visitedHashTable[thisHash].append(thisState)

        #check if state is goal
        if(goalCheck(thisState)):
            foundGoal = thisState
            break

        if(report and thisState.depth == nextReport):
            print("Depth Report: " + str(thisState.depth))
            nextReport+=10
    
        #need to add successors
        successorStates = successorGenerator(thisState)

        for successor in successorStates:
            stateQ.pushBack(successor)
            # stateQ.push(successor, getHeuristicPriority(successor))
            
    return foundGoal

def y2019d18(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d18.txt"
    print("2019 day 18:")

    lineList = []

    with open(inputPath) as f:
        for line in f:
            lineList.append(line.strip())
        
    #parse the maze
    wallsList = []
    doorList = []
    keyList = []
    start = None
    for y in range(len(lineList)):
        for x in range(len(lineList[y])):
            c = lineList[y][x]
            if(c == '#'):
                wallsList.append((x,y))
            elif(c == "."):
                continue
            elif(str.isupper(c)):
                doorList.append((x,y))
            elif(str.islower(c)):
                keyList.append((x,y))
            elif(c == "@"):
                start = (x,y)
            else:
                raise ValueError("Illegal input character: " + str(c))
    
    #build the initial key door list
    kdList = []

    for key in keyList:
        #find the matching door
        v = str.upper(lineList[key[1]][key[0]])
        for door in doorList:
            if(lineList[door[1]][door[0]] == v):
                kdList.append(KeyDoor(key, door))
                break
        
    startState = MazeState(start, kdList)

    successorGenerator = lambda x:generateSuccessorStates(x, wallsList)

    foundGoal = None
    # foundGoal = searchLoop(startState, successorGenerator, isGoalState, True)
        
    if(foundGoal == None):
        print("(Part 1) No Goal found before all states explored.")  
    else:
        print("Min distance (part 1): " + str(foundGoal.depth))

    #start on part 2
    #only need to change the state representation and the successor generation

    wallsListPart2 = copy.copy(wallsList)
    
    def newWallsGenerator():
        k = [(-1,0), (0,0), (1,0),(0,-1), (0,1)]
        for kk in k:
            yield kk
        
    for t in newWallsGenerator():
        newWall = (start[0]+t[0], start[1]+t[1])
        assert(newWall not in wallsListPart2)
        wallsListPart2.append(newWall)

    
    def isValidUpperLeft(start, pos):
        if(pos[1] > start[1]):
            return False
        if(pos[0] > start[0]):
            return False
        return True

    def isValidUpperRight(start, pos):
        if(pos[1] > start[1]):
            return False
        if(pos[0] < start[0]):
            return False
        return True

    def isValidLowerLeft(start, pos):
        if(pos[1] < start[1]):
            return False
        if(pos[0] > start[0]):
            return False
        return True

    def isValidLowerRight(start, pos):
        if(pos[1] < start[1]):
            return False
        if(pos[0] < start[0]):
            return False
        return True

    transforms = [(-1,-1),(1,-1),(-1,1),(1,1)]
    validators = [isValidUpperLeft, isValidUpperRight, isValidLowerLeft, isValidLowerRight]
    results = [None]*4

    for i in range(4):
        transform = transforms[i]
        startTemp = (start[0]+transform[0], start[1]+transform[1])

        #construct a modified key door lis
        newKDList = []

        for kd in kdList:
            if(validators[i](startTemp, kd.k)):
                newKDList.append(kd)

        print("KDLen: " + str(len(newKDList)))

        startStateTemp = MazeState(startTemp, newKDList)
        results[i] = searchLoop(startStateTemp, successorGenerator, isGoalState, False)
        # print("DING")

    #the distance is the sum of all 4 distances where
    #each robot's distance is concerned solely with the key/door pairs fully in its quadrant

    dTotal = 0
    for r in results:
        if(r == None):
            print("(Part 2) Failed to locate a goal for quadrant:" + str(results.index(r)))
        else:
            print(str(r.depth))
            dTotal+=r.depth
    
    print("Min distance (Part 2): " + str(dTotal))
    #part 2: 10464 - sound wrong, havent checked

    print("===========")