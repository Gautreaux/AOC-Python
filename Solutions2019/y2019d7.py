import itertools
import asyncio
from typing import Optional

from .IntcodeLib import *
from AOC_Lib.SolutionBase import Answer_T


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


class Solution_2019_07(IntcodeSolutionBase):
    """https://adventofcode.com/2019/day/7"""


    def _test_one_config(self, config: tuple[int, ...]) -> int:
        """Test one config and return amount of thrust"""

        runners = buildLinkedRunners(self.program, len(config))
            
        # push starting values
        for r,c in zip(runners, config):
            r._input_q.put_nowait(c)

        # push the second input for the first item
        runners[0]._input_q.put_nowait(0)

        fut = asyncio.gather(*map(lambda x: x.run(), runners))

        asyncio.get_event_loop().run_until_complete(fut)
            
        return runners[-1].getOutputQ().get_nowait()

    def _test_once_config_pt2(self, config: tuple[int, ...]) -> int:
        """Test one config and return amount of thrust"""

        runners = buildLinkedRunners(self.program, len(config))

        # push starting values
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

        v = None

        while not q.empty():
            v = q.get_nowait()

        if v is None:
            raise RuntimeError('No Output was produced')

        for t in tasks:
            t.cancel()

        return v

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        NUM_AMPS = 5

        return max(map(
            lambda x: self._test_one_config(x),
            itertools.permutations(range(NUM_AMPS), NUM_AMPS),
        ))

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        NUM_AMPS = 5

        print("{} Doing part 2. This will be slow".format(
            self.__class__.__name__,
        ))

        return max(map(
            lambda x: self._test_once_config_pt2(x),
            itertools.permutations(
                map(lambda x: x+5, range(NUM_AMPS)),
                NUM_AMPS,
            )
        ))
