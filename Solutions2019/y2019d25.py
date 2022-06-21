
from typing import Generator
from .IntcodeLib import IntcodeProgram, IntcodeRunner

import asyncio
from collections import deque

async def waitThenPrompt(event: asyncio.Event, push_q: asyncio.Queue):
    """Wait for an event to signal that input is needed,
    thn collect the input and push it to the provided queue"""

    inputs = [
        "south",
        "take mouse",
        "north",
        "west",
        "north",
        "west",
        "south",
        "take hypercube",
        "north",
        "east",
        "north",
        "west",
        "take semiconductor",
        "east",
        "south",
        "south",
        "west",
        "take antenna",
        "west",
        "south",
        "south",
        "inv",
        "south",
    ]

    def _inp_generator() -> Generator[bytes, None, None]:
        for k in inputs:
            if not k.endswith('\n'):
                k = f"{k}\n"
            yield k.encode('ascii')
        while True:
            i = input(">")
            if not i.endswith('\n'):
                i = f"{i}\n"
            yield i.encode('ascii')
    _g = _inp_generator()

    while True:
        await event.wait()
        event.clear()
        bts = next(_g)
        print(bts)
        for b in bts:
            await push_q.put(b)


async def echoOutput(in_q: asyncio.Queue, event: asyncio.Event, pattern: str = "Command?"):
    """Collect output from `in_q` and when `pattern` is see, signal event"""
    dq = deque(maxlen=len(pattern))

    while True:
        b = await in_q.get()
        c = chr(b)
        print(c, end="", flush=True)
        dq.append(c)

        if pattern == "".join(map(str, dq)):
            event.set()


def interactiveMode(runner: IntcodeRunner):
    """Run in interactive mode"""

    loop = asyncio.get_event_loop()
    ready_for_input = asyncio.Event()

    echo_task = loop.create_task(echoOutput(runner.getOutputQ(), ready_for_input))
    prompt_task = loop.create_task(waitThenPrompt(ready_for_input, runner.getInputQ()))
    run_task = loop.create_task(runner.run())

    done, pending = loop.run_until_complete(asyncio.wait(
        [prompt_task, echo_task, run_task], return_when=asyncio.FIRST_COMPLETED
    ))


    if run_task.done():
        pass
    else:
        print("WARNING, one of the tasks exited unexpectedly.\n"
            "  Pending is {}".format(pending))

    for t in pending:
        t.cancel()

    return (20483, None)


def y2019d25(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d25.txt"
    print("2019 day 25:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    prog = IntcodeProgram(map(int, lineList[0].split(",")))
    runner = IntcodeRunner(prog)

    # TODO - automate (actually write the search(s))

    return interactiveMode(runner)
    return (20483, None)

    # for multi line inputs

    return (Part_1_Answer, Part_2_Answer)