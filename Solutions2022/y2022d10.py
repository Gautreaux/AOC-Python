
from dataclasses import dataclass, field
from enum import unique, Enum
from typing import Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T


@unique
class Instructions(Enum):
    NOOP = 0
    ADDX = 1

    @property
    def cycles_to_complete(self) -> int:
        """Return number of cycles needed to complete this instruction"""
        if self == Instructions.NOOP:
            return 1
        elif self == Instructions.ADDX:
            return 2
        else:
            raise NotImplementedError(self)


@dataclass(frozen=True)
class CrtCpuInstruction:
    """A Single instruction and relevant parameters"""

    instruction: Instructions
    param: int


CrtCpuProgram = list[CrtCpuInstruction]


def parse_program(lines: list[str]) -> CrtCpuProgram:
    """Parse the program and return"""
    program = []

    # The number of tokens in the longest instruction
    LONGEST_INSTRUCTION = 2

    for line in lines:
        line = line.strip()
        
        if not line:
            # Skip empty line:
            continue

        tokens: list[str] = line.split(" ")

        while len(tokens) < LONGEST_INSTRUCTION:
            tokens.append('-1')

        program.append(CrtCpuInstruction(
            Instructions[tokens[0].upper()],
            *map(int, tokens[1:]),
        ))

    return program

@dataclass
class CrtCpu:
    """Cathode Ray Tube CPU"""

    program: CrtCpuProgram
    
    x_register: int = 1

    # What instruction are we executing
    program_counter: int = 0

    # How many cycles remain on this specific instruction execution
    _cycles_remain: int = field(default=0, init=False, compare=False, hash=False)

    # How many cycles have elapsed
    _cycles_counter: int = field(default=0, init=False, compare=False, hash=False)

    @classmethod
    def build_cpu(cls, lines: list[str]):
        """Parse a program from a list of lines and return a CPU loaded with that program"""
        return cls(program=parse_program(lines))

    @property
    def active_instruction(self) -> CrtCpuInstruction:
        """Return the active instruction"""
        return self.program[self.program_counter]

    def _cycle(self):
        """Run one cycle"""

        self._pre_cycle_hook()
        self._cycles_counter += 1
        
        # Adjust the remaining cycles            
        instr = self.active_instruction
        assert self._cycles_remain >= 1
        self._cycles_remain -= 1

        self._mid_cycle_hook()
        
        try:
            # Execute the instruction
            if instr.instruction == Instructions.NOOP:
                return
            elif instr.instruction == Instructions.ADDX:
                if self._cycles_remain == 0:
                    self.x_register += instr.param
                return
            else:
                raise NotImplementedError(instr.instruction)
        finally:
            self._post_cycle_hook()

    def _run(self):
        """Run the program"""

        self._cycles_remain = self.active_instruction.instruction.cycles_to_complete

        while True:
            self._cycle()
            if self._cycles_remain <= 0:
                self.program_counter += 1
                if self.program_counter >= len(self.program):
                    # We are out of bounds on the program
                    return
                elif self.program_counter < 0:
                    # Preemptive in expectation of a part 2
                    raise RuntimeError("Out of bounds, probably should terminate")
                self._cycles_remain = self.active_instruction.instruction.cycles_to_complete

    def _pre_cycle_hook(self):
        """Hook called once before each cycle begins,
        * before the cycle counter has been incremented and the 
        * before the cycle remaining has been decremented
            for overriding in derived classes
        """

    def _mid_cycle_hook(self):
        """Hook called once during each cycle,
        * after the cycle counter has been incremented
        * after the cycle remaining has been decremented
            for overriding in derived classes
        """
    
    def _post_cycle_hook(self):
        """Hook called once after each cycle completes
        * after the cycle counter has been incremented
        * after the cycle remaining has been decremented
        * after registers are updated with any changes
        * before the new instruction is loaded (program counter increments, cycles remain reset)
            for overriding in derived classes
        """


@dataclass
class CrtCpu_2022_10(CrtCpu):

    signal_strengths: list[int] = field(default_factory=list, init=False, hash=False, compare=False)

    def _mid_cycle_hook(self):

        if self._cycles_counter in range(20, 221, 40):
            self.signal_strengths.append(self.x_register * self._cycles_counter)
        
        # Part 2 Drawing        
        current_x_coord = (self._cycles_counter-1) % 40

        if abs(current_x_coord - self.x_register) <= 1:
            chr_to_print = '█'
        else:
            chr_to_print = ' '
        print(chr_to_print, end=('\n' if current_x_coord == 39 else ''))


class Solution_2022_10(SolutionBase):
    """https://adventofcode.com/2022/day/10"""

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        cpu = CrtCpu_2022_10.build_cpu(self.input_str_list())
        cpu._run()

        assert len(cpu.signal_strengths) == 6
        return sum(cpu.signal_strengths)


    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        print("\nFor Part 2, Read the letters from the console above.\n")
        return "EZFPRAKL"
