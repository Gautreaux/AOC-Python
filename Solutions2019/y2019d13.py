import math
import random

from Solutions2019.y2019d5 import y2019d5

def get2dHash(pos):
    return hash(pos[0]*10000+pos[1])

class GameState():
    def __init__(self):
        self.blockList = []
        self.blockCount = 0
        self.xValue = None
        self.yValue = None
        self.score = None

        self.memMap = {}

        self.minX = 0
        self.minY = 0
        self.maxX = 0
        self.maxY = 0

        self.charmap = {0:" ", 1:"█", 2:"B", 3:"_", 4:"."}

    def __del__(self):
        pass

    def sendCommand(self):
        self.draw()
        i = input("Move: ") 
        if(i == 'l'):
            return -1
        elif(i == 'r'):
            return 1
        elif(i == ""):
            return 0
        else:
            return self.draw()

    def draw(self):
        vList = []
        for y in range(self.minY, self.maxY+1):
            for x in range(self.minX, self.maxX+1):
                if(get2dHash((x,y)) in self.memMap):
                    print(self.charmap[self.memMap[get2dHash((x,y))]], end = "")
                else:
                    print(self.charmap[0], end = "")
            print("")

    def receiveCommand(self, c):
        if(self.xValue == None):
            self.xValue = int(c)
            return
        
        if(self.yValue == None):
            self.yValue = int(c)
            return

        #this is the third element
        tileID = int(c)
        pos = (self.xValue, self.yValue)
        self.xValue = None
        self.yValue = None
        if(pos == (-1, 0)):
            self.score = tileID
            if(len(self.blockList) == 0):
                print("Block list empty. Score (part2): " + str(self.score))
            return
        else:
            if(tileID == 2):
                if pos not in self.blockList:
                    self.blockList.append(pos)
            else:
                if pos in self.blockList:
                    self.blockList.remove(pos)

        if(pos[0] < self.minX):
            self.minX = pos[0]
        if(pos[0] > self.maxX):
            self.maxX = pos[0]
        if(pos[1] < self.minY):
            self.minY = pos[1]
        if(pos[1] > self.maxY):
            self.maxY = pos[1]

        self.memMap[get2dHash(pos)] = tileID




def y2019d13(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d13.txt"
    print("2019 day 13:")

    with open(inputPath) as f:
        for line in f:
            #do something
            #TODO - read a single line properly
            myLine = line.strip()
            break

    gameState = GameState()

    y2019d5(inputPath, inputFunction=gameState.sendCommand,outputFunction=gameState.receiveCommand)

    print(len(gameState.blockList))

    print("===========")

    #part 1: 399 incorrect