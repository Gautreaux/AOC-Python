from AOC_Lib.SolutionBase import InputSpecification, InputType
import itertools
from typing import Callable, Iterable, Iterator, Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T


class FFTRunner:
    """Runs rounds of Flawed Frequency Transmission"""

    def __init__(self, dimension: int) -> None:

        self.dimension = dimension

        # pre build and compute functions for reach row
        # This is a little magic so lets explain
        #
        # In each iteration, each output digit is a fixed mapping
        #   against the input digits
        # Rather than actually building the pattern, we can jump to doing
        #   lookups against the input positions
        #   and skip all the times zero operations
        #       which is many of them
        # This is done with a lambda reduce
        #   so that the "minimum" amount of operations is done

        print(f"Dimension is {dimension}")

        _INTERVAL = 1

        current_positive = set()
        current_negative = set()

        # Stores the 'compiled' functions
        operators: list[Callable[[list[int], int, int], tuple[int, int]]] = []

        # will produce functions that do minimum amounts of work to get the answer
        def change_function_factory(
            positive_needed: set[int], negative_needed: set[int]
        ):

            nonlocal current_positive
            nonlocal current_negative

            positive_to_add = list(positive_needed - current_positive)
            positive_to_remove = list(current_positive - positive_needed)

            negative_to_add = list(negative_needed - current_negative)
            negative_to_remove = list(current_negative - negative_needed)

            current_positive = positive_needed
            current_negative = negative_needed

            def change_function(
                in_list: list[int], positive_sum: int, negative_sum: int
            ) -> tuple[int, int]:

                new_pos = (
                    positive_sum
                    + sum(map(lambda x: in_list[x], positive_to_add))
                    - sum(map(lambda x: in_list[x], positive_to_remove))
                )

                new_negative = (
                    negative_sum
                    + sum(map(lambda x: in_list[x], negative_to_add))
                    - sum(map(lambda x: in_list[x], negative_to_remove))
                )

                return (new_pos, new_negative)

            return change_function

        for n in range(dimension):
            # pattern = self.pattern_factory(n+1)
            # slice = itertools.islice(pattern, dimension)
            # pattern_and_pos = enumerate(slice)
            # remove_zeros = filter(lambda x: x[1] != 0, pattern_and_pos)
            # rz_list = list(remove_zeros)
            # positive_items = set(map(lambda x: x[0], filter(lambda x: x[1] == 1, rz_list)))
            # negative_items = set(map(lambda x: x[0], filter(lambda x: x[1] == -1, rz_list)))

            positive_items, negative_items = self.better_pattern_factory(
                n + 1, dimension
            )

            operators.append(change_function_factory(positive_items, negative_items))

            if (len(operators) % _INTERVAL) == 0:
                print(f"'Compiled' {len(operators)} / {dimension} Operators")

        print(f"Finished Building Operators")
        assert len(operators) == dimension

        def _output_fn(in_list: list[int]) -> list[int]:
            """Do one round of FFT"""
            running_pos = 0
            running_neg = 0

            to_return = []
            for op in operators:
                running_pos, running_neg = op(in_list, running_pos, running_neg)
                to_return.append(self.clamp(running_pos - running_neg))
            return to_return

        self._output_fn = _output_fn
        print(f"Done 'compiling' for dimension {dimension}")

    @classmethod
    def clamp(cls, value: int) -> int:
        """Clamp `n` to the proper domain"""
        return abs(value) % 10

    @classmethod
    def pattern_factory(
        cls, n: int, base_pattern: Iterable[int] = [0, 1, 0, -1]
    ) -> Iterator[int]:
        """Produce the pattern for Flawed Frequency Transmission"""

        assert n != 0

        # Based on the previous solution the following magic works.
        #   its magic so who really knows
        #   for x in itertools.count():
        #       return base_pattern[((x+1)//n)%len(base_pattern)]

        # Iterator based variant

        # repeat the base pattern forever:
        base_forever = itertools.cycle(base_pattern)

        # expand each element `n` times
        expand_n = map(lambda x: itertools.repeat(x, n), base_forever)

        # chain into a single iterator
        as_iter = itertools.chain.from_iterable(expand_n)

        # remove the first element
        next(as_iter)

        # and return that iterator
        return as_iter

    @classmethod
    def better_pattern_factory(cls, n: int, max: int) -> tuple[set[int], set[int]]:
        """Produce the pattern for Flawed Frequency Transmission, but smart

        Returns two sets: the indexes of positive items and the indexes of negative items
        """

        assert n != 0

        step_amount = 4 * n

        positive_start = n - 1
        negative_start = 3 * n - 1

        # print(f"N {n}, Step: {step_amount}: {positive_start}, {negative_start}")

        def get_set(this_start: int) -> set[int]:
            positive_series_starts = itertools.takewhile(
                lambda x: x < max, itertools.count(start=this_start, step=step_amount)
            )

            expand = itertools.chain.from_iterable(
                map(lambda x: range(x, x + n), positive_series_starts)
            )

            return set(filter(lambda x: x < max, expand))

        return (get_set(positive_start), get_set(negative_start))

    def n_rounds(
        self, n: int, in_list: list[int], report_interval: Optional[int] = 10
    ) -> list[int]:
        """Run `n` rounds and return the result"""

        assert n > 0
        assert len(in_list) == self.dimension

        if n == 0:
            return in_list
        last = in_list
        for x in range(n):
            if report_interval and ((x % report_interval) == 0):
                print(f"Progress: {x}/{n}")

            last = self._output_fn(last)
        return last

    def one_round(self, in_list: list[int]) -> list[int]:
        """Run one round and return the result"""
        return self.n_rounds(1, in_list)


class Solution_2019_16(SolutionBase):
    """https://adventofcode.com/2019/day/16"""

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        val = list(map(int, self.input_str().strip()))

        runner = FFTRunner(len(val))

        val = runner.n_rounds(100, val)

        return "".join(map(str, val[:8]))

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        val = list(
            map(
                int,
                itertools.chain.from_iterable(
                    itertools.repeat(
                        self.input_str().strip(),
                        10000,
                    )
                ),
            )
        )

        runner = FFTRunner(len(val))

        val = runner.n_rounds(100, val, report_interval=1)

        offset = int(self.input_str()[:7])

        return "".join(map(str, itertools.islice(val, offset, offset + 8)))


def printNice(l: list[int]):
    print("[{}]".format(",".join(map(lambda x: "{:>2}".format(str(x)), l))))


for i in range(16):
    printNice(list(itertools.islice(FFTRunner.pattern_factory(i + 1), 32)))

print("================")

for i in range(8):
    printNice(list(itertools.islice(FFTRunner.pattern_factory(i + 1), 8)))

print("================")

debug = "12345678"

fr = FFTRunner(len(debug))

val = debug

for _ in range(4):
    print(val)
    new_val = fr.one_round(list(map(int, val)))
    new_val = "".join(map(str, new_val))
    print(new_val)
    val = new_val
    print("- - - - - -")


print("==============")
s1 = Solution_2019_16(
    input_spec=InputSpecification(
        InputType.BYTES, bytes_content=b"03036732577212944063491565474664"
    )
)
print("Test part 2: ", s1.part_2_answer)
print("==============")
s2 = Solution_2019_16(
    input_spec=InputSpecification(
        InputType.BYTES, bytes_content=b"02935109699940807407585447034323"
    )
)
print("Test part 2: ", s2.part_2_answer)
print("==============")
print(s1.part_2_answer)
print(s2.part_2_answer)
print("==============")
exit(0)
# Part 2:
#   bigger than 11156704
