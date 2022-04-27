from .IntcodeLib import *
import itertools
import asyncio


def buildLinkedRunners(prog: IntcodeProgram, qty:int) -> list[IntcodeRunner]:
    """Return a list of runners where the output of one runner is linked to the input of the next"""
    runners: list[IntcodeRunner] = []

    # build intcode runners
    while len(runners) < qty:
        if not runners:
            r_new = IntcodeRunner(prog)
            runners.append(r_new)
        else:
            # build new runners linking the inputs together
            r_new = IntcodeRunner(prog, in_q=runners[-1].getOutputQ())
            runners.append(r_new)
    return runners

def y2019d7(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d7.txt"
    print("2019 day 7:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    prog = IntcodeProgram(map(int, lineList[0].split(",")))

    max_thrust = 0

    NUM_AMPS = 5

    for config in itertools.permutations(range(NUM_AMPS), NUM_AMPS):

        runners = buildLinkedRunners(prog, NUM_AMPS)
            
        # push starting values
        for r,c in zip(runners, config):
            r._input_q.put_nowait(c)

        # push the second input for the first item
        runners[0]._input_q.put_nowait(0)

        fut = asyncio.gather(*map(lambda x: x.run(), runners))

        asyncio.get_event_loop().run_until_complete(fut)
            
        sc = runners[-1].getOutputQ().get_nowait()
        max_thrust = max(sc, max_thrust)

    Part_1_Answer = max_thrust

    max_thrust_2 = 0

    last_start = (4,4)

    for config in itertools.permutations(range(5, 5 + NUM_AMPS), NUM_AMPS):
        if config[:2] != last_start:
            last_start = config[:2]
            print(f"Starting: ", last_start)
        runners = buildLinkedRunners(prog, NUM_AMPS)

        # push starting valuse
        for r,c in zip(runners, config):
            r._input_q.put_nowait(c)

        # create the tee
        q = asyncio.Queue()
        t = queueTee(runners[-1].getOutputQ(), [runners[0].getInputQ(), q])

        # push the start instruction
        runners[0].getInputQ().put_nowait(0)

        loop = asyncio.get_event_loop()

        tasks = []
        tasks.append(loop.create_task(t))

        for r in runners:
            tasks.append(loop.create_task(r.run()))

        loop.run_until_complete(runUntilHalt(runners, 0.1))

        while not q.empty():
            v = q.get_nowait()
            max_thrust_2 = max(v, max_thrust_2)

        for t in tasks:
            t.cancel()   
        
    Part_2_Answer = max_thrust_2

    return (Part_1_Answer, Part_2_Answer)