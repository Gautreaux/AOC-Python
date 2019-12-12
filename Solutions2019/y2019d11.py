import math

from Solutions2019.y2019d5 import y2019d5

#TODO - this should use a general 2d grid class for memory
#       or even better, a list class that can be indexed via pairs
class painterBot():
    def __init__(self):
        self.xPos = 0
        self.yPos = 0
        self.orientation = 0
        self.commandsReceived = 0
        self.robotMemory = {}
        # self.paintCount = 0
        self.visitList = []

        self.minX = 0
        self.minY = 0
        self.maxX = 0
        self.maxY = 0

    def __del__(self):
        pass

    def getPosHash(self, overridePos = None):
        'return the hash of the position'

        #return hash((self.xPos, self.yPos))
        #this hash causes collisions ^

        if(overridePos == None):
            overridePos = (self.xPos,self.yPos)

        return((overridePos[0]*100000+overridePos[1]))

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
            # if(self.getPosHash() not in self.robotMemory):
            #     self.paintCount+=1

            self.robotMemory[self.getPosHash()] = c
            self.visitList.append([self.xPos, self.yPos, self.getPosHash()])
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

            if(self.xPos < self.minX):
                self.minX = self.xPos
            if(self.yPos < self.minY):
                self.minY = self.yPos
            if(self.xPos > self.maxX):
                self.maxX = self.xPos
            if(self.yPos > self.maxY):
                self.maxY = self.yPos

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

        from Solutions2019.debug.debug2019d11 import validateVisitList as VVL

        if(VVL(myRobot.visitList, False)):
            print("Part1: The visit list validates successfully.")
        else:
            print("Part1: The visit list failed to validate.")

        print("Part 1:" + str(len(myRobot.robotMemory)))
        # print(myRobot.paintCount)

        #create a new robot for part 2
        myRobot = painterBot()
        myRobot.robotMemory[myRobot.getPosHash((0,0))] = 1

        #rerun again
        y2019d5(inputPath, inputFunction=myRobot.sendCommand,outputFunction=myRobot.receiveCommand)

        if(VVL(myRobot.visitList, False)):
            print("Part2: The visit list validates successfully.")
        else:
            print("Part2: The visit list failed to validate.")

        #now we need to print the value
        #step 1: recover the bounds of the image
        #this initally involved hashing and a 2-d search
        #   that never really worked, so we just tracked it in the class
        
        #step 2: print

        #step 2.1 - build the y list
        #need to convert y so that it prints max to min
        yList = []
        for y in range(myRobot.minY, myRobot.maxY+1):
            yList.append(y)

        yList.reverse()

        for y in yList:
            for x in range(myRobot.minX, myRobot.maxX+1):
                thisHash = myRobot.getPosHash((x,y))
                if(thisHash in myRobot.robotMemory):
                    if(myRobot.robotMemory[thisHash] == 0):
                        print(" ", end = "")
                    else:
                        print("█", end="")
                else:
                    print(" ", end="")
            print("")


    print("===========")

    #part 1: 4 incorrect
    #          691 incorrect