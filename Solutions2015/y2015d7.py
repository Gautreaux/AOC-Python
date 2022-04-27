# from AOC_Lib.name import *

import asyncio
from collections import defaultdict, namedtuple
from pickle import NONE
from types import coroutine
from typing import Any, Union

# string or int
SoI_t = Union[str, int]

CircuitComponent = namedtuple("CircuitComponent", "out_name operator arg1 arg2")

async def constantInput(value: Any, q: asyncio.Queue, name = None):
    """Return a coroutine that continually pushes `value` into `q`
        NOTE: q must be bounded or program may deadlock
    """
    while True:
        # print(f"DING input {name}")
        await q.put(value)


async def bitwiseNOT16(in_q: asyncio.Queue, out_q: asyncio.Queue, name = None):
    """Take the first value from in_q, do bitwise NOT, pad to 16 digits, 
        and push that into the out_q forever
        NOTE: out_q must be bounded or program may deadlock
    """
    in_val = await in_q.get()
    in_q.task_done()
    s = "{:016b}".format(in_val)
    if len(s) > 16:
        print("WARNING: found a too long value in bitwiseNot: {}".format(in_val))
        s = s[:16] 
    out_s = "".join(map(lambda x: "0" if x == "1" else "1", s))
    out_val = int(out_s, 2)
    while True:
        # print(f"DING not {name}:{out_val}")
        await out_q.put(out_val)


async def bitwiseAND(in_q: asyncio.Queue, in_b_q: asyncio.Queue, out_q: asyncio.Queue, name = None):
    """Take the first value from each of the in queues,
        do the bitwise and,
        and push that value into the output forever
    """
    in_val = await in_q.get()
    in_q.task_done()
    in_b_val = await in_b_q.get()
    in_b_q.task_done()
    out_val = in_val & in_b_val
    while True:
        # print(f"DING and {name}:{out_val}")
        await out_q.put(out_val)


async def bitwiseOR(in_q: asyncio.Queue, in_b_q: asyncio.Queue, out_q: asyncio.Queue, name = None):
    """Take the first value from each of the in queues,
        do the bitwise or,
        and push that value into the output forever
    """
    in_val = await in_q.get()
    in_q.task_done()
    in_b_val = await in_b_q.get()
    in_b_q.task_done()
    out_val = in_val | in_b_val
    while True:
        # print(f"DING or {name}:{out_val}")
        await out_q.put(out_val)


async def lshift16(in_q : asyncio.Queue, lshift_amt: int, out_q: asyncio.Queue, name = None):
    """Take the first value from in_q, leftshift by lshift_amt, crop to 16 digits,
        and push that value into the out_q forever
        NOTE: out_q must be bounded or program may deadlock
    """
    in_val = await in_q.get()
    in_q.task_done()
    out_val = in_val << lshift_amt
    out_val & 0xffff
    while True:
        # print(f"DING lshift {name}:{out_val}")
        await out_q.put(out_val)

        
async def rshift16(in_q : asyncio.Queue, rshift_amt: int, out_q: asyncio.Queue, name = None):
    """Take the first value from in_q, rightshift by rshift_amt,
        and push that value into the out_q forever
        NOTE: out_q must be bounded or program may deadlock
    """
    in_val = await in_q.get()
    in_q.task_done()
    out_val = in_val >> rshift_amt
    while True:
        # print(f"DING rshift {name}:{out_val}")
        await out_q.put(out_val)


async def passthrough(in_q: asyncio.Queue, out_q: asyncio.Queue, name = None):
    """Pass values from one queue to another queue
        NOTE: out_q must be bounded or program may deadlock
    """
    # this is due to a possible edge case with multiple redirections
    # ex: on the input:
    #   a -> c
    #   100 -> a
    #   a -> b
    while True:
        val = await in_q.get()
        in_q.task_done()
        # print(f"DING passthrough {name}:{val}")
        await out_q.put(val)

async def out_debug(q, name):
    i = await q.get()
    q.task_done()
    print(f"OUT DEBUG GOT VALUE: {name} {i}")


def tryConvert(s: str) -> SoI_t:
    try:
        return int(s)
    except ValueError:
        return s.strip()

def parseValidateInput(lines: str) -> list[CircuitComponent]:
    """Parse the input and return it as the format
        (<out name>, <operator>, <arg 1 (lhs)>, <arg 2 (rhs)>)
    """

    out_list = []

    for l in lines:
        lhs, rhs = l.split(" -> ")
        out_name = tryConvert(rhs)
        assert(isinstance(out_name, str))

        if " " not in lhs:
            out_list.append(CircuitComponent(out_name, "CONST", tryConvert(lhs), None))
            continue
        
        tokens = lhs.split(" ")

        if len(tokens) == 2:
            assert(tokens[0] == "NOT")
            out_list.append(CircuitComponent(out_name, tokens[0], tryConvert(tokens[1]), None))
        elif len(tokens) == 3:
            out_list.append(CircuitComponent(out_name, tokens[1], tryConvert(tokens[0]), tryConvert(tokens[2])))
        else:
            raise ValueError("Could not parse line: `{}`".format(l))
    return out_list


async def heartbeat(q_map):
    """Debug function, prints resolved values"""
    await asyncio.sleep(10) 
    while True:
        resolved_group = {}
        for k,v in q_map.items():
            try:
                g = v.get_nowait()
                resolved_group[k] = g
            except:
                pass
        print("The resolved set is: {}".format(resolved_group))
        await asyncio.sleep(2)


def buildCoroutines(parsed: list[CircuitComponent], q_map, skip_list: list[str] = []) -> list[Any]:
    """Build the coroutine objects using the parsed list and the provided q_map
        skip_list: list of items to skip building coroutine for
    """
    coroutines = []

    for p in parsed:
        if p.out_name in skip_list:
            print(f"WARN: skipping `{p.out_name}`")
            continue

        if p.operator == "CONST":
            assert(p.arg2 is None)
            if isinstance(p.arg1, int):
                coroutines.append(constantInput(p.arg1, q_map[p.out_name], str(p)))
            else:
                coroutines.append(passthrough(q_map[p.arg1], q_map[p.out_name], str(p)))
        elif p.operator == "NOT":
            assert(p.arg2 is None)
            assert(isinstance(p.arg1, str))
            coroutines.append(bitwiseNOT16(q_map[p.arg1], q_map[p.out_name], str(p)))
        elif p.operator == "RSHIFT":
            assert(isinstance(p.arg2, int))
            assert(isinstance(p.arg1, str))
            coroutines.append(rshift16(q_map[p.arg1], p.arg2, q_map[p.out_name], str(p)))
        elif p.operator == "LSHIFT":
            assert(isinstance(p.arg2, int))
            assert(isinstance(p.arg1, str))
            coroutines.append(lshift16(q_map[p.arg1], p.arg2, q_map[p.out_name], str(p)))
        elif p.operator == "AND":
            coroutines.append(bitwiseAND(q_map[p.arg1], q_map[p.arg2], q_map[p.out_name], str(p)))
        elif p.operator == "OR":
            coroutines.append(bitwiseOR(q_map[p.arg1], q_map[p.arg2], q_map[p.out_name], str(p)))
        else:
            raise ValueError("Do not know how to handle the circuit input: {}".format(p))
        
    return coroutines


def addMissingIntGenerators(q_map, coroutines: list[any]) -> int:
    int_vals = set()
    for k,v in q_map.items():
        if isinstance(k, int):
            if k in int_vals:
                continue
            int_vals.add(k)
            coroutines.append(constantInput(k, v, f"CONST INT {k}"))

    print("Added handlers for the set: {}".format(int_vals))
    return len(int_vals)


def runUntilSignal(coroutines, q_map, n: str) -> Any:
    """Run until there is a signal on wire n
        return the value of the signal
    """

    if n not in q_map:
        raise RuntimeError("There is nothing for the out variable ({}), this will deadlock".format(n))

    futures = []

    # get or start an event loop
    loop = asyncio.get_event_loop()

    for f in coroutines:
        futures.append(asyncio.ensure_future(f, loop=loop))

    try:
        return loop.run_until_complete(q_map[n].get())
    except KeyboardInterrupt:
        print("Killing coroutines")
        for f in futures:
            # we can't
            f.cancel()

        # flush the queues so that things close appropriately
        for _ in range(3):
            for q in q_map.items():
                try:
                    q.put_nowait(-1)
                except:
                    pass
        raise


def y2015d7(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d7.txt"
    print("2015 day 7:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    # we could do a topological ordering 
    #   but thats not nearly as much fun as abusing
    #   the asyncio library to do stuff for us
    # this also has the benefit of waiting 

    # index of all the queues we have, by name
    #   each queue is from input
    q_map = defaultdict(lambda: asyncio.Queue(1))

    parsed = parseValidateInput(lineList)

    # list of all the circuit components
    #   in case they are needed later
    coroutines = buildCoroutines(parsed, q_map)

    assert(len(coroutines) == len(parsed))

    addMissingIntGenerators(q_map, coroutines)

    coroutines.append(heartbeat(q_map))
    coroutines.append(out_debug(q_map['c'], "c(0)"))
    coroutines.append(out_debug(q_map['a'], "a"))

    Part_1_Answer = runUntilSignal(coroutines, q_map, 'a')

    q_map_2 = defaultdict(lambda: asyncio.Queue(1))

    coroutines_2 = buildCoroutines(parsed, q_map_2, ['b'])
    coroutines_2.append(constantInput(Part_1_Answer, q_map_2['b']))

    assert(len(coroutines_2) == len(parsed))

    addMissingIntGenerators(q_map_2, coroutines_2)

    coroutines_2.append(heartbeat(q_map_2))
    coroutines_2.append(out_debug(q_map_2['c'], "c(0)"))
    coroutines_2.append(out_debug(q_map_2['b'], f"b({Part_1_Answer})"))
    coroutines_2.append(out_debug(q_map_2['a'], "a"))

    Part_2_Answer = runUntilSignal(coroutines_2, q_map_2, 'a')

    return (Part_1_Answer, Part_2_Answer)