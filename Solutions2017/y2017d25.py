# from AOC_Lib.name import *


from collections import defaultdict, namedtuple
from enum import Enum, unique
from tqdm import tqdm
from typing import Iterator, Optional

Memory_T = defaultdict[int, int]

Action_T = namedtuple("Action_T", "t arg")

State_T = namedtuple("State_T", "name zero_actions one_actions")


@unique
class ActionEnum(Enum):
    """Type of actions"""
    WRITE = 'W'
    MOVE = 'M'
    CONTINUE = 'C'


def parseActions(itr: Iterator[str], expect_pred: Optional[int] = None) -> list[Action_T]:
    """Parse all Actions and return"""
   
    to_return: list[Action_T] = []

    n = next(itr)
    a,_,b = n.rpartition(" ")
    assert(a == "If the current value is")

    if expect_pred is not None:
        assert(int(b[:-1]) == expect_pred)

    n = next(itr)
    a,_,b = n.rpartition(" ")
    assert(a.startswith("- Write the value"))
    b = int(b[:-1])
    to_return.append(Action_T(t=ActionEnum.WRITE, arg=b))

    n = next(itr)
    a,_,b = n.rpartition(" ")
    assert(a.startswith("- Move one slot to"))
    b = 1 if b == "right." else -1
    to_return.append(Action_T(t=ActionEnum.MOVE, arg=b))

    n = next(itr)
    a,_,b = n.rpartition(" ")
    assert(a.startswith("- Continue with state"))
    b = b[:-1]
    to_return.append(Action_T(t=ActionEnum.CONTINUE, arg=b))

    return to_return


def parseState(itr: Iterator[str]) -> State_T:
    """Parse a State and return"""

    n = next(itr)
    while (n.strip() == ""):
        n = next(itr)
    
    a,b,s = n.split()
    assert(a == "In")
    assert(b == "state")
    state_name = s[:-1]

    zero_actions = parseActions(itr, expect_pred=0)
    one_actions = parseActions(itr, expect_pred=1)

    return State_T(
        name=state_name,
        zero_actions=zero_actions,
        one_actions=one_actions
    )


def calculateChecksum(mem: Memory_T) -> int:
    """Calculate and return the checksum for the memory"""
    # Would hope that there are no `0` in memory, but be sure
    return sum(1 for _ in filter(
        lambda x: x != 0,
        mem.values(),
    ))


def y2017d25(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2017/d25.txt"
    print("2017 day 25:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    i = iter(lineList)

    start_state = next(i).split()[-1][:-1]
    checksum_time = int(next(i).split()[-2])
    assert(next(i).strip() == "")

    states_index: dict[str, State_T] = {}

    while True:
        try:
            s = parseState(i)
            n = s.name
            assert(n not in states_index)
            states_index[n] = s
        except StopIteration:
            break
    
    print(f"Starting in {start_state}, running {checksum_time} rounds")

    memory: Memory_T = defaultdict(int)

    current_ptr: int = 0
    current_state: State_T = states_index[start_state]

    for i in tqdm(range(checksum_time)):
        v = memory[current_ptr]

        if v == 0:
            actions = current_state.zero_actions
        elif v == 1:
            actions = current_state.one_actions
        else:
            raise ValueError(f"Should not be possible {v}")

        for a in actions:
            x = a.t
            y = a.arg
            if x == ActionEnum.WRITE:
                if y == 0:
                    memory.pop(current_ptr)
                else:
                    memory[current_ptr] = y
            elif x == ActionEnum.MOVE:
                current_ptr += y
            elif x == ActionEnum.CONTINUE:
                current_state = states_index[y]
                continue
            else:
                raise RuntimeError(f"Unrecognized Action Type: {x}")

    Part_1_Answer = calculateChecksum(memory)

    return (Part_1_Answer, Part_2_Answer)