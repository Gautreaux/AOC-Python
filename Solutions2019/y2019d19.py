import asyncio
import functools
import itertools

from .IntcodeLib import IntcodeProgram, IntcodeRunner


def y2019d19(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d19.txt"
    print("2019 day 19:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    prog = IntcodeProgram(map(int, lineList[0].split(",")))
    loop = asyncio.get_event_loop()

    @functools.cache
    def checkPosInBeam(x: int, y: int) -> bool:
        """Return True iff the point is inside the beam"""
        runner = IntcodeRunner(prog)
        run_task = loop.create_task(runner.run())
        runner.getInputQ().put_nowait(x)
        runner.getInputQ().put_nowait(y)
        runner.runTillBlockOrExit(run_task, loop)
        assert(runner.getOutputQ().qsize() == 1)
        out_val = runner.getOutputQ().get_nowait()
        if out_val == 1:
            return True
        elif out_val == 0:
            return False
        else:
            raise RuntimeError("Should be unreachable")

    pos_in_beam = set()
    for y in range(50):
        for x in range(50):
            if checkPosInBeam(x,y):
                pos_in_beam.add((x,y))
                print("#", end="")
            else:
                print(".", end="")
        print("")

    Part_1_Answer = len(pos_in_beam)

    # theres probably a math way to find this easier 
    #   by getting an approximating line
    #   but whatever

    # objective: find the upper right of the 100x100 region
    #   posit: it will be the top of its column

    # TODO - finalize    

    return (Part_1_Answer, Part_2_Answer)