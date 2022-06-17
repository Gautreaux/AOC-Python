
from typing import Any, Callable

STATE_T = Any

def CycleAndRemainder(
    start_state: STATE_T,
    next_state_generator: Callable[[STATE_T], STATE_T],
    target_state_number: int,
    cycle_threshold: int = 10000,
) -> tuple[STATE_T, STATE_T]:
    """Advance `target_state` times of `start_state`, exploiting the cyclic nature"""

    state = start_state

    cache = {}

    cache[state] = 0

    for i in range(1, cycle_threshold):
        state = next_state_generator(state)
        if i == target_state_number:
            return state
        elif state in cache:
            # pass

    # TODO - finish
    # TODO - integrate y2018d12

raise RuntimeError("Need to finish Cycle and remainder")