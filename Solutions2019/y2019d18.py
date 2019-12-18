import copy
from AOC_Lib.queue import Queue

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

class MazeState():
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
        if(self.pos != other.pos):
            return False
        if(self.kList != other.kList):
            return False
        return True

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

    visitedHashTable = {}
    stateQ = Queue()
    stateQ.pushBack(startState)
    foundGoal = None

    nextReport = 0

    while(len(stateQ) > 0):
        thisState = stateQ.pop()
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
        if(isGoalState(thisState)):
            foundGoal = thisState
            break

        if(thisState.depth == nextReport):
            print("Depth Report: " + str(thisState.depth))
            nextReport+=10
    
        #need to add successors
        successorStates = generateSuccessorStates(thisState, wallsList)

        for successor in successorStates:
            stateQ.pushBack(successor)
        
    if(foundGoal == None):
        print("No Goal found before all states explored")  
    else:
        print("Min distance (part 1): " + str(foundGoal.depth))
        
    print("===========")