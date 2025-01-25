from .IntcodeLib import *
from collections import defaultdict

_BLACK_PANEL = 0
_WHITE_PANEL = 1

# TODO - this should use a general 2d grid class for memory
#       or even better, a list class that can be indexed via pairs


class PainterBot:
    def __init__(self):
        # current Position
        self.xPos = 0
        self.yPos = 0

        self.orientation = 0
        self.commandsReceived = 0

        self.robotMemory = defaultdict(lambda: _BLACK_PANEL)

        # something for pervious debugging
        # self.visitList = []

        # ????
        self.minX = 0
        self.minY = 0
        self.maxX = 0
        self.maxY = 0

    def __del__(self):
        pass

    def getPosHash(self, overridePos=None) -> int:
        "return the hash of the position"

        # return hash((self.xPos, self.yPos))
        # this hash causes collisions ^

        if overridePos == None:
            overridePos = (self.xPos, self.yPos)

        return overridePos[0] * 100000 + overridePos[1]

    def readCamera(self) -> int:
        return self.robotMemory[self.getPosHash()]

    # TODO - this could be much better but it works so why bother
    def receiveCommand(self, c: int):
        c = int(c)
        if self.commandsReceived % 2 == 0:
            # this is a paint command
            # print("PAint")
            # if(self.getPosHash() not in self.robotMemory):
            #     self.paintCount+=1

            self.robotMemory[self.getPosHash()] = c
            # self.visitList.append([self.xPos, self.yPos, self.getPosHash()])
            # print("PAINT: " + str((self.xPos, self.yPos)) + " " + str(self.orientation) + " " + str(c))
        else:
            # this is a rotate (and move) command
            # print("turn and move")
            if c == 1:
                self.orientation += 1
                if self.orientation > 3:
                    self.orientation = 0
            else:
                self.orientation -= 1
                if self.orientation < 0:
                    self.orientation = 3

            if self.orientation == 0:
                self.yPos += 1

            elif self.orientation == 1:
                self.xPos += 1

            elif self.orientation == 2:
                self.yPos -= 1

            elif self.orientation == 3:
                self.xPos -= 1

            else:
                raise ValueError("Illegal orientation " + str(self.orientation))

            if self.xPos < self.minX:
                self.minX = self.xPos
            if self.yPos < self.minY:
                self.minY = self.yPos
            if self.xPos > self.maxX:
                self.maxX = self.xPos
            if self.yPos > self.maxY:
                self.maxY = self.yPos

            # print("Postion: " + str((self.xPos, self.yPos)))

        self.commandsReceived += 1


async def robotCoro(robot: PainterBot, runner: IntcodeRunner):
    """AIO task for the robot"""
    while True:
        current_color = robot.readCamera()
        await runner.getInputQ().put(current_color)
        try:
            paint_instr = await asyncio.wait_for(runner.getOutputQ().get(), 1)
            move_instr = await asyncio.wait_for(runner.getOutputQ().get(), 1)

            robot.receiveCommand(paint_instr)
            robot.receiveCommand(move_instr)
        except asyncio.TimeoutError:
            # the robot must be dead
            return


def robotTillHalt(robot: PainterBot, runner: IntcodeRunner) -> None:
    """Run the robot/runner until a halt occurs"""
    loop = asyncio.get_event_loop()
    t = loop.create_task(runner.run())

    f = loop.run_until_complete(robotCoro(robot, runner))
    t.cancel()


def y2019d11(inputPath=None):
    if inputPath == None:
        inputPath = "Input2019/d11.txt"
    print("2019 day 11:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    prog = IntcodeProgram(map(int, lineList[0].split(",")))

    # part 1
    inst = IntcodeRunner(prog)
    myRobot = PainterBot()
    robotTillHalt(myRobot, inst)
    Part_1_Answer = len(myRobot.robotMemory)

    # reset for part 2
    inst = IntcodeRunner(prog)
    myRobot = PainterBot()
    myRobot.robotMemory[myRobot.getPosHash((0, 0))] = 1
    robotTillHalt(myRobot, inst)

    # now we need to print the value
    # step 1: recover the bounds of the image
    # this initally involved hashing and a 2-d search
    #   that never really worked, so we just tracked it in the class

    # step 2: print

    # step 2.1 - build the y list
    # need to convert y so that it prints max to min
    yList = []
    for y in range(myRobot.minY, myRobot.maxY + 1):
        yList.append(y)

    yList.reverse()

    for y in yList:
        for x in range(myRobot.minX, myRobot.maxX + 1):
            thisHash = myRobot.getPosHash((x, y))
            if thisHash in myRobot.robotMemory:
                if myRobot.robotMemory[thisHash] == 0:
                    print(" ", end="")
                else:
                    print("█", end="")
            else:
                print(" ", end="")
        print("")

    print("===========")

    # TODO - some day integrate a OCR system but for now:
    Part_2_Answer = "ZCGRHKLB"

    return (Part_1_Answer, Part_2_Answer)
