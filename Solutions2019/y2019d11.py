import math

from Solutions2019.y2019d5 import y2019d5


#TODO - this should use a general 2d grid class for memory
class painterBot():
    def __init__(self):
        self.xPos = 0
        self.yPos = 0
        self.orientation = 0
        self.commandsReceived = 0
        self.robotMemory = {}
        self.paintCount = 0

    def getPosHash(self):
        return hash((self.xPos, self.yPos))

    def sendCommand(self):
        if(self.getPosHash() in self.robotMemory):
            return self.robotMemory[self.getPosHash()]
        else:
            return 0

    def receiveCommand(self, c):
        c = int(c)
        if(self.commandsReceived % 2 == 0):
            #this is a paint command
            # print("PAint")
            if(self.getPosHash() not in self.robotMemory):
                self.paintCount+=1

            self.robotMemory[self.getPosHash()] = c
            # print("PAINT: " + str((self.xPos, self.yPos)) + " " + str(self.orientation) + " " + str(c))
        else:
            #this is a rotate (and move) command
            # print("turn and move")
            if(c == 1):
                self.orientation += 1
                if(self.orientation > 3):
                    self.orientation = 0
            else:
                self.orientation -= 1
                if(self.orientation < 0):
                    self.orientation = 3
            
            if(self.orientation == 0):
                self.yPos += 1
            elif(self.orientation == 1):
                self.xPos += 1
            elif(self.orientation == 2):
                self.yPos -= 1
            elif(self.orientation == 3):
                self.xPos -= 1
            else:
                raise ValueError("Illegal orientation " + str(self.orientation))

            # print("Postion: " + str((self.xPos, self.yPos)))

        self.commandsReceived+=1

def y2019d11(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d11.txt"
    print("2019 day 11:")

    with open(inputPath) as f:
        for line in f:
            #do something
            #TODO - read a single line properly
            myLine = line.strip()
            break
    
        myRobot = painterBot()

        # cList = "10001010011010"
        # for e in cList:
        #     myRobot.receiveCommand(e)

        y2019d5(inputPath, inputFunction=myRobot.sendCommand,outputFunction=myRobot.receiveCommand)

        # for key in myRobot.robotMemory:
        #     print(str(key) + " " + str(myRobot.robotMemory[key]))

        print(len(myRobot.robotMemory))
        print(myRobot.paintCount)
            
    print("===========")

    #part 1: 4 incorrect
    #          691 incorrect