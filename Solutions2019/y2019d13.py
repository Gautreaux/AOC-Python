import math

from Solutions2019.y2019d5 import y2019d5


class GameState():
    def __init__(self):
        self.blockList = []
        self.blockCount = 0
        self.xValue = None
        self.yValue = None


    def __del__(self):
        pass

    def sendCommand(self):
        pass

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
        if(tileID == 2):
            if pos not in self.blockList:
                self.blockList.append(pos)
        else:
            if pos in self.blockList:
                self.blockList.remove(pos)


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