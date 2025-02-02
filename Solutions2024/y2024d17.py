from typing import Optional, Iterable
from tqdm import tqdm


from AOC_Lib.SolutionBase import SolutionBase, Answer_T

# from multiprocessing import Pool


class CronospatialComputer:
    def __init__(
        self, program: Iterable[int], register_a: int, register_b: int, register_c: int
    ) -> None:
        self.register_a: int = register_a
        self.register_b: int = register_b
        self.register_c: int = register_c
        self.instruction_pointer: int = 0
        self.program: tuple[int, ...] = tuple(program)
        self.output: list[int] = []

    def reset(self, register_a: int = 0):
        """Reset the computer and optionally supply a value for `a`"""
        self.register_a = register_a
        self.register_b = 0
        self.register_c = 0
        self.instruction_pointer = 0
        self.output.clear()

    def _resolve_combo_operand(self) -> int:
        """Resolve the value for the combo operand"""
        v = self.program[self.instruction_pointer + 1]
        match (v):
            case 0:
                return 0
            case 1:
                return 1
            case 2:
                return 2
            case 3:
                return 3
            case 4:
                return self.register_a
            case 5:
                return self.register_b
            case 6:
                return self.register_c
            case _:
                raise ValueError(f"Invalid combo operand: {v}")

    def _adv(self):
        """Handle the adv instruction (opcode 0)"""
        combo = self._resolve_combo_operand()
        self.register_a = self.register_a // (2**combo)
        self.instruction_pointer += 2

    def _bxl(self):
        """Handle the bxl instruction (opcode 1)"""
        literal = self.program[self.instruction_pointer + 1]
        self.register_b = self.register_b ^ literal
        self.instruction_pointer += 2

    def _bst(self):
        """Handle the bst instruction (opcode 2)"""
        combo = self._resolve_combo_operand()
        self.register_b = combo & 0b111
        self.instruction_pointer += 2

    def _jnz(self):
        """Handle the jnz instruction (opcode 3)"""
        literal = self.program[self.instruction_pointer + 1]
        if self.register_a == 0:
            self.instruction_pointer += 2
        else:
            self.instruction_pointer = literal

    def _bxc(self):
        """Handle the bxc instruction (opcode 4)"""
        # From the problem description:
        # > For legacy reasons, this instruction reads an operand but ignores it.
        combo = self._resolve_combo_operand()  # noqa W0612 Unused Variable

        self.register_b = self.register_b ^ self.register_c
        self.instruction_pointer += 2

    def _out(self):
        """Handle the out instruction (opcode 5)"""
        combo = self._resolve_combo_operand()
        self.output.append(combo & 0b111)
        self.instruction_pointer += 2

    def _bdv(self):
        """Handle the bdv instruction (opcode 6)"""
        combo = self._resolve_combo_operand()
        self.register_b = self.register_a // (2**combo)
        self.instruction_pointer += 2

    def _cdv(self):
        """Handle the cdv instruction (opcode 7)"""
        combo = self._resolve_combo_operand()
        self.register_c = self.register_a // (2**combo)
        self.instruction_pointer += 2

    def _step(self) -> None:
        """Step once"""
        v = self.program[self.instruction_pointer]
        match (v):
            case 0:
                self._adv()
            case 1:
                self._bxl()
            case 2:
                self._bst()
            case 3:
                self._jnz()
            case 4:
                self._bxc()
            case 5:
                self._out()
            case 6:
                self._bdv()
            case 7:
                self._cdv()
            case _:
                raise ValueError(f"Invalid operator: {v}")

    def run(self) -> str:
        """Run the program until termination"""
        try:
            while True:
                self._step()
        except IndexError:
            pass

        return ",".join(map(str, self.output))

    def run_check_output(self, goal: str) -> str | None:
        """Run the program until termination"""
        try:
            while True:
                last_sz = len(self.output)
                self._step()
                if len(self.output) != last_sz:
                    # This was an output step
                    #   see if it matches
                    if not goal.startswith(",".join(map(str, self.output))):
                        # This cannot produce the correct output
                        return None
        except IndexError:
            pass

        return ",".join(map(str, self.output))


_CHUNK_SIZE = 1_000_000


def _worker(args):
    goal: str = args[0]
    chunk_id: int = args[1]
    start = chunk_id * _CHUNK_SIZE

    computer = CronospatialComputer(map(int, goal.split(",")), 0, 0, 0)
    for o in range(_CHUNK_SIZE):
        computer.reset(register_a=(start + o))
        result = computer.run_check_output(goal)
        if result is None:
            continue
        if result == goal:
            return start + o
        else:
            print("a={} | result={} | goal={}".format((start + o), result, goal))

    print(f"No result in range {start} {start + _CHUNK_SIZE-1}")

    return None


class Solution_2024_17(SolutionBase):
    """https://adventofcode.com/2024/day/17"""

    def __post_init__(self):
        """Runs Once After `__init__`"""
        lines = self.input_str_list(include_empty_lines=True)

        try:
            a = int(lines[0].rpartition(" ")[-1])
            b = int(lines[1].rpartition(" ")[-1])
            c = int(lines[2].rpartition(" ")[-1])
            prog = [int(t) for t in (lines[4].rpartition(" ")[-1]).split(",")]
        except IndexError:
            raise RuntimeError("Input Probably Malformed") from None

        self.computer: CronospatialComputer = CronospatialComputer(prog, a, b, c)
        self.original_a_value: int = self.computer.register_a

        # Sample
        # self.computer.program = tuple([int(t) for t in '0,3,5,4,3,0'.split(',')])
        # self.computer.register_a = 117440

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        return self.computer.run()

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        goal = ",".join(map(str, self.computer.program))

        # Did not work
        #   so probably some error / trick I'm missing
        ten_mil = 10_000_000_000

        num_chunks = ten_mil // _CHUNK_SIZE

        print(f"Chunk size is {_CHUNK_SIZE}; Num Chunks is {num_chunks}")

        # # Unbounded chunk generation
        # def chunk_gen() -> Iterator[int]:
        #     for i in itertools.count(start=0):
        #         yield i * _CHUNK_SIZE

        params = [(goal, c) for c in range(num_chunks)]

        # Multiprocess for each in params
        from multiprocessing import Pool, Process, cpu_count

        with Pool() as pool:
            results = list(tqdm(pool.imap(_worker, params), total=len(params)))
            results = [r for r in results if r is not None]

        # 18323965 - too low

        return min(results)

        raise NotImplementedError(
            "Let run to ~370 million; need a multiprocessor or there is some bug/trick I missed"
        )
