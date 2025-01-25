from typing import Any, Callable


SearchFn_T = Callable[[int], int]


class DiscreteSearch:
    """
    Search through Discrete Space, looking for values

    SearchFn must be stateless
    """

    def __init__(self, fn: SearchFn_T) -> None:
        self._fn = fn

    def _increasing_common(self, start: int, selector: Callable[[int], bool]) -> int:
        """Common worker for less than and less than or equal to"""

        # check that the starting value is valid
        last_guess = start
        last_result = self._fn(start)

        if not selector(last_result):
            raise RuntimeError("The start value is already not a valid solution")

        best_guess = last_guess

        incr = 1

        while True:
            new_guess = best_guess + incr
            new_result = self._fn(new_guess)

            if selector(new_result):
                # The new value is valid so
                #   we take that as the new best
                #   and double incr to search more
                incr *= 2
                best_guess = new_guess
            elif incr == 1:
                # we stepped by one and failed
                #   so `best_guess` is best we can do
                return best_guess
            else:
                # we went over the limit
                # so reduce the increment and retry
                incr = incr // 2

    def find_biggest_less_than(self, target: int, hint: int = 0) -> int:
        """Find the biggest value V that satisfies
        `fn(V) < target`

        Start with `V=hint`
        """
        return self._increasing_common(start=hint, selector=lambda x: x < target)

    def find_biggest_less_than_equal_to(self, target: int, hint: int = 0) -> int:
        """Find the biggest value V that satisfies
        `fn(V) <= target`

        Start with `V=hint`
        """
        return self._increasing_common(start=hint, selector=lambda x: x <= target)
