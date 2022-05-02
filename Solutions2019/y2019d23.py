import asyncio

from .IntcodeLib import IntcodeProgram, IntcodeRunner

from random import randint

_push_lock = asyncio.Lock()

async def PushRouter(q: asyncio.Queue, network_addresses: dict[int, asyncio.Queue]):
    """Listen and construct the three-byte messages on q; send to the appropriate address"""
    while True:
        address = await q.get()
        q.task_done()
        x_value = await q.get()
        q.task_done()
        y_value = await q.get()
        q.task_done()

        if address == 255:
            print("Sending y value to address 255: {}".format(y_value))
            return y_value
        
        if address not in network_addresses:
            raise RuntimeError(f"Unsupported network address: {address}")

        # use no-wait to prevent yielding the event loop
        #   and packets getting out of order
        # added a lock for good measure too
        async with _push_lock:
            network_addresses[address].put_nowait(x_value)
            network_addresses[address].put_nowait(y_value)


async def RandomNegOne(runners: dict[int, IntcodeRunner]):
    """Randomly find blocked NICs and push instructions"""
    while True:
        await asyncio.sleep(.05)
        async with _push_lock:
            for _ in range(5):
                i = randint(0, 49)
                if runners[i].isIOBlocked():
                    runners[i].getInputQ().put_nowait(-1)
                    break


def y2019d23(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d23.txt"
    print("2019 day 23:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    prog = IntcodeProgram(map(int, lineList[0].split(",")))

    network_addresses = {}
    runners = {}

    loop = asyncio.get_event_loop()

    task_list = []

    for i in range(50):
        q = asyncio.Queue()
        network_addresses[i] = q
        q.put_nowait(i)
        runner = IntcodeRunner(prog, in_q=q)
        task_list.append(loop.create_task(PushRouter(runner.getOutputQ(), network_addresses)))
        runners[i] = runner
        task_list.append(loop.create_task(runner.run()))

    task_list.append(RandomNegOne(runners))
        
    done, pending = loop.run_until_complete(asyncio.wait(
        task_list, return_when=asyncio.FIRST_COMPLETED
    ))



    return (Part_1_Answer, Part_2_Answer)