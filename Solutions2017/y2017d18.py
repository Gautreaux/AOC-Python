# from AOC_Lib.name import *

import asyncio
from collections import defaultdict
from typing import Optional


class Duet:
    def __init__(self, program, in_q=None, out_q=None) -> None:
        self._program = program
        self._instr_ptr = 0
        self._last_send = None
        self._memory = defaultdict(int)
        self._is_done = False
        self._in_q: Optional[asyncio.Queue] = in_q
        self._out_q: Optional[asyncio.Queue] = out_q
        self._number_sends = 0
        self._is_io_blocked = False

    @property
    def last_snd(self) -> int:
        return self._last_send

    @property
    def is_io_blocked(self) -> int:
        return self._is_io_blocked

    @property
    def number_sends(self) -> int:
        return self._number_sends

    def setRegister(self, register: str, value: int):
        assert len(register) == 1
        self._memory[register] = value

    async def _run_cycle(self):
        instr, arg1, arg2 = self._program[self._instr_ptr]

        if type(arg1) == int:
            arg1_value = arg1
        else:
            arg1_value = self._memory[arg1]

        if type(arg2) == int:
            arg2_value = arg2
        else:
            arg2_value = self._memory[arg2]

        if instr == "snd":
            # print(f"SND {arg1_value}")
            self._last_send = arg1_value

            if self._out_q is not None:
                self._is_io_blocked = True
                await self._out_q.put(arg1_value)
                self._number_sends += 1
                self._is_io_blocked = False
        elif instr == "set":
            assert type(arg1) != int
            # print(f"SET {arg1} {arg2_value}")
            self._memory[arg1] = arg2_value
        elif instr == "add":
            # print(f"ADD {arg1} {arg2_value}")
            assert type(arg1) != int
            self._memory[arg1] += arg2_value
        elif instr == "mul":
            # print(f"MUL {arg1} {arg2_value}")
            assert type(arg1) != int
            self._memory[arg1] *= arg2_value
        elif instr == "mod":
            # print(f"MOD {arg1} {arg2_value}")
            assert type(arg1) != int
            self._memory[arg1] %= arg2_value
        elif instr == "rcv":
            if self._in_q is None:
                # this is part 1 so terminate
                self._is_done = True
            else:
                self._is_io_blocked = True
                in_val = await self._in_q.get()
                self._in_q.task_done()
                self._is_io_blocked = False
                self._memory[arg1] = in_val
        elif instr == "jgz":
            if arg1_value > 0:
                self._instr_ptr += arg2_value - 1
        self._instr_ptr += 1

    async def run(self):
        while not self._is_done:
            if self._instr_ptr < 0 or self._instr_ptr >= len(self._program):
                self._is_done = True
                return
            await self._run_cycle()

    def run_sync(self):
        asyncio.get_event_loop().run_until_complete(self.run())


def y2017d18(inputPath=None):
    if inputPath == None:
        inputPath = "Input2017/d18.txt"
    print("2017 day 18:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    prog = []

    for l in lineList:
        s = l.split(" ")

        for i, v in enumerate(s):
            try:
                s[i] = int(v)
            except ValueError:
                pass

        if len(s) < 3:
            s.append(None)

        prog.append(tuple(s))

    # just to make it non-editable
    prog = tuple(iter(prog))

    d = Duet(prog)
    d.run_sync()
    Part_1_Answer = d._last_send

    # =================

    q_0_to_1 = asyncio.Queue()
    q_1_to_0 = asyncio.Queue()

    d_0 = Duet(prog, in_q=q_1_to_0, out_q=q_0_to_1)
    d_0.setRegister("p", 0)
    d_1 = Duet(prog, in_q=q_0_to_1, out_q=q_1_to_0)
    d_1.setRegister("p", 1)

    async def watchdog():
        while True:
            await asyncio.sleep(0.1)
            if d_0.is_io_blocked and d_1.is_io_blocked:
                # need to validate that queues are empty
                #   due to a race condition with how the switches occur
                if q_0_to_1.qsize() == 0 and q_1_to_0.qsize() == 0:
                    # programs are deadlocked
                    print("Watchdog found deadlock, terminating")
                    return
            if d_0._is_done and d_1._is_done:
                return

    loop = asyncio.get_event_loop()

    futures = []
    futures.append(loop.create_task(d_0.run()))
    futures.append(loop.create_task(d_1.run()))
    futures.append(loop.create_task(watchdog()))

    done, pending = loop.run_until_complete(
        asyncio.wait(futures, return_when=asyncio.FIRST_COMPLETED)
    )

    if futures[-1] in pending:
        print("[WARNING] does not look like a clean exit")

    for p in pending:
        p.cancel()

    print(done)

    Part_2_Answer = d_1.number_sends

    return (Part_1_Answer, Part_2_Answer)
