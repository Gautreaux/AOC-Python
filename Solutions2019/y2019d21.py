# from AOC_Lib.name import *

import itertools
from typing import Optional
from .IntcodeLib import IntcodeProgram, IntcodeRunner


def printDeath(o: list[int]) -> None:
    """Print when a death occurred"""
    print("".join(map(chr, o)))


def didEndInDeath(o: list[int]) -> bool:
    """Return `True` iff this run ended in death"""
    return (o[-1] < 128)


def runSpringCode(
    spring_code_program: list[str],
    intcode_program: IntcodeProgram,
    execute_command: str
) -> Optional[int]:
    """Run the spring code program amd Return the spring code result if one exists"""
    assert(len(spring_code_program) <= 15)

    to_send = list(map(ord, itertools.chain(
        "\n".join(spring_code_program),
        "\n", # to separate code and command
        execute_command,
    )))

    if to_send[-1] != ord('\n'):
        # execute command did not end in '\n'
        to_send.append(ord('\n'))
    
    runner = IntcodeRunner(intcode_program)
    o = runner.run_sync(to_send)

    if didEndInDeath(o):
        printDeath(o)
        return None
    else:
        return o[-1]

def y2019d21(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d21.txt"
    print("2019 day 21:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    prog = IntcodeProgram(map(int, lineList[0].split(",")))

    my_spring_script = [
        # check if need to jump
        "NOT A J",
        "NOT B T",
        "OR T J",
        "NOT C T",
        "OR T J",
        # check if can jump
        "AND D J",
    ]

    Part_1_Answer = runSpringCode(my_spring_script, prog, "WALK")

    if Part_1_Answer is None:
        return (Part_1_Answer, Part_2_Answer)

    my_spring_script = [
        # We want to jump whenever:
        # TODO - jumping opportunistically (like above) doesnt seem to work
        #   need to jump only when it is required
        "NOT A J",
        "NOT B T",
        ""

    ]

    Part_2_Answer = runSpringCode(my_spring_script, prog, "RUN")

    return (Part_1_Answer, Part_2_Answer)

# ==================


from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum, IntEnum, unique
from functools import reduce, cache
import itertools
from operator import mul
from typing import Any, Callable, Iterator, Type, TypeVar, Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from AOC_Lib.Geometry.Point import DiscretePoint2
from AOC_Lib.SlidingWindow import sliding_window
from .IntcodeLib import IntcodeSolutionBase


SpringCodeInst_T = str
SpringCodeProgram_T = list[SpringCodeInst_T]



@dataclass(frozen=True)
class InputCondition:
    A: bool
    B: bool
    C: bool
    D: bool
    E: bool
    F: bool
    G: bool
    H: bool
    I: bool

    @classmethod
    def iter_all_options(cls) -> Iterator['InputCondition']:
        """Iterate over all options"""
        for t in itertools.product(*map(lambda _: [True, False], range(9))):
            yield InputCondition(*t)

    def __str__(self) -> str:
        return "".join(map(
            lambda x: "█" if x else " ",
            [self.A, self.B, self.C, self.D, self.E, self.F, self.G, self.H, self.I]
        ))

    def __iter__(self) -> Iterator[bool]:
        yield self.A
        yield self.B
        yield self.C
        yield self.D
        yield self.E
        yield self.F
        yield self.G
        yield self.H
        yield self.I

@unique
class Action(IntEnum):
    # EITHER = 0b11
    JUMP = 0b01
    STEP = 0b10
    IGNORE = 0b00
    AMBIGUOUS = 0b11111111111


@dataclass(frozen=True)
class Rule:
    selector: Callable[[InputCondition], bool]
    action: Action
    description: str

def auto_determine_solution():
    """some tools for automatically inferring solution"""

    print('\n\n')

    def filter_four_gap(i: InputCondition) -> bool:
        """Return `True` iff there is a 4-long gap"""
        l = list(i)
        for s in sliding_window(l,4):
            if any(s):
                # There exists some solid somewhere in this window
                continue
            else:
                return True
        return False

    def filter_specific_factory(*args) -> Callable[[InputCondition], bool]:
        """Build a check for a specific condition"""
        assert len(args) == 9
        return lambda i: all(map(lambda a,b: a == b, i, args))

    def filter_double_jump_trap(i: InputCondition) -> bool:
        """Ignore a pattern of inputs that always leads to trapping"""
        
        must_jump = (i.A is False) or (i.B is False) or (i.C is False)
        if not must_jump:
            return False # This filter does not apply

        must_double_jump = i.F is False
        if not must_double_jump:
            return False
        
        double_jump_traps = (i.H is False) and (i.I is False)
        # if double jump traps, then this is all trap. Filter this test
        return double_jump_traps

    rules: list[Rule] = [
        Rule(lambda i: i.A is False, Action.JUMP, "Jump if step would die"),
        Rule(lambda i: i.D is False, Action.STEP, "Step if jump would die"),
        Rule(lambda i: i.A and i.B and i.C and i.D, Action.STEP, "No Action Required"),
        Rule(lambda i: i.A and i.B is False and i.D and i.E, Action.JUMP, 'Greedy jump'),
        # Rule(lambda i: i.A and i.B and i.C is False and i.D and i.E is False and i.F and i.H is False, Action.STEP, "Step when jump is trap"),
        # Rule(lambda i: i.C is False and i.D and i.E and i.F, Action.JUMP, 'Greedy Jump 2a'),
        Rule(lambda i: i.A and i.C is False and i.D and i.E, Action.JUMP, 'Greedy Jump 2b'),
        Rule(lambda i: i.A and i.B is False and i.D and i.E is False and i.H, Action.JUMP, 'Must Jump'),
        Rule(lambda i: i.A and i.B and i.C is False and i.D and i.E is False and i.F is False, Action.JUMP, 'Jump when step would lead to trap'),
        Rule(lambda i: i.A and i.B and i.C is False and i.D and i.E is False and i.F and i.G and i.H, Action.STEP, 'Defer Jump 1'),
        Rule(filter_specific_factory(True, True, False, True, False, True, False, True, True), Action.JUMP, 'Jump when better'),

        # Some other checks
        Rule(lambda i: i.D and i.E is False and i.H is False, Action.STEP, 'Step if jump would trap'),
        # Rule(lambda i: i.D and i.E and i.F is False and i.H is False and i.I is False, Action.STEP, 'Step if jump would trap 2'),

        # Items to ignore because all solutions end in death:
        #  These need to be very selective in what they ignore to
        #   avoid discarding things that may matter
        Rule(lambda i: i.A is False and i.D is False, Action.IGNORE, "Any Action Dies Next"),
        Rule(lambda i: i.A is False and i.D and i.E is False and i.H is False, Action.IGNORE, "Any Action Dies Soon"),
        Rule(lambda i: i.A and i.B is False and i.C is False and i.D and i.E and i.F is False, Action.IGNORE, "Any Action Dies Soon 2"),
        Rule(filter_four_gap, Action.IGNORE, "SKIP 4 Gap"),
        Rule(filter_double_jump_trap, Action.IGNORE, 'Skip when double jump will trap'),

        # Specific Conditions I am confident we can ignore
        Rule(filter_specific_factory(True, True, False, True, False, False, True, False, True), Action.IGNORE, "Specific1"),

        # The one condition where there is not a good answer
        Rule(filter_specific_factory(True, True, False, True, False, True, False, True, False), Action.AMBIGUOUS, 'AMBIGUOUS')
    ]

    # Assert all rules have a unique name
    assert len(set(map(lambda r: r.description, rules))) == len(rules)

    inputs_with_no_rule: list[InputCondition] = []
    inputs_to_action: dict[InputCondition, Action] = {}

    total_checked = 0
    total_ignored = 0
    total_conflict = 0
    total_ambiguous = 0
    total_no_action = 0

    for input in InputCondition.iter_all_options():
        relevant_rules = list(filter(lambda r: r.selector(input), rules))
        
        total_checked += 1

        has_ignore = any(map(lambda x: x.action == Action.IGNORE, relevant_rules))
        if has_ignore:
            # Skip this test case for some reason
            total_ignored += 1
            continue

        if not relevant_rules:
            inputs_with_no_rule.append(input)

        has_jump = any(map(lambda x: x.action == Action.JUMP, relevant_rules))
        has_step = any(map(lambda x: x.action == Action.STEP, relevant_rules))
        has_ambiguous = any(map(lambda x: x.action == Action.AMBIGUOUS, relevant_rules))

        if has_ambiguous:
            total_ambiguous += 1
            assert all(map(lambda x: x.action == Action.AMBIGUOUS, relevant_rules))
            continue
        elif (not has_jump) and (not has_step):
            total_no_action += 1
            continue
        elif has_jump and not has_step:
            inputs_to_action[input] = Action.JUMP
            continue
        elif has_step and not has_jump:
            inputs_to_action[input] = Action.STEP
            continue
     
        total_conflict += 1
        if total_conflict <= 3:
            print(f"Found conflicting rules for input.")
            print("  ABCDEFGHI")
            print(f"  {input}")
            for r in relevant_rules:
                print(f"   {r.action.name} by {r.description}")
    print(f"Tested {total_checked}")
    print(f"  Ignored  : {total_ignored}")
    print(f"  Conflict : {total_conflict}")
    print(f"  No Action: {total_no_action}")
    print(f"  Ambiguous: {total_ambiguous}")
    if inputs_with_no_rule:
        print(f"WARNING: {len(inputs_with_no_rule)} inputs where no rule was applied")
        print(" ", "ABCDEFGHI")
        for i in range(min(len(inputs_with_no_rule), 10)):
            print(" ", inputs_with_no_rule[i])
    print('\n\n')

    # Check for any redundant rules
    
    
    # Build a mapping of input to applied rules
    inputs_to_rule: dict[InputCondition, set[Rule]] = {}
    for i in inputs_to_action.keys():
        s = set()
        for r in rules:
            if r.selector(i):
                s.add(r)
        inputs_to_rule[i] = s

    # Flatten the iterable into a collection of rules
    step_and_jump_rules = set(itertools.chain.from_iterable(inputs_to_rule.values()))
    assert all(map(lambda r: r.action in [Action.JUMP, Action.STEP], step_and_jump_rules))

    # Find rules that appear alone (these _must_ be kept)
    single_rules: set[Rule] = set()
    for rule_set in inputs_to_rule.values():
        if len(rule_set) == 1:
            single_rules.add(next(iter(rule_set)))
    if single_rules:
        print(f"The following {len(single_rules)} rules (of {len(step_and_jump_rules)}) are unique selectors:")
        for r in single_rules:
            print(f"  {r.description}")
    else:
        print("There are no single rules.")

    # Check each non-single rule to see if it is always covered by a single rule:
    # Check if each input has at least one of the single rules
    print("Checking for rules that can be safely removed...")
    for r in step_and_jump_rules - single_rules:
        has_uncovered_instance = False
        for i,rs in inputs_to_rule.items():
            # this rule is not applied to this input, so skip
            if r not in rs:
                continue
            if rs.intersection(single_rules):
                # this rule is covered by a single rule
                #   so for this particular input it is safe to discard this rule
                continue
            else:
                has_uncovered_instance = True
        if has_uncovered_instance is False:
            print(f"  {r.description} - Safe to Remove")



class Solution_2019_21(IntcodeSolutionBase):
    """https://adventofcode.com/2019/day/21"""

    def _run_spring_code(
        self,
        spring_code_program: SpringCodeProgram_T,
        execute_command: str
    ):
        """Run spring code and return result if one exists"""
        assert(len(spring_code_program) < 15)

        to_send = list(map(ord, itertools.chain(
            '\n'.join(spring_code_program),
            '\n', # to separate code and command
            execute_command
        )))

        if to_send[-1] != ord('\n'):
            # execute command did not end in '\n'
            to_send.append(ord('\n'))
        
        runner = self._runner_factory()
        o = runner.run_sync(to_send)

        # Check if we ended in death
        if o[-1] < 128: # type: ignore
            print("".join(map(chr, o))) # type: ignore
        else:
            return o[-1]


    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        # Actually made by hand with thought

        my_spring_script = [
            # check if need to jump
            "NOT A J",
            "NOT B T",
            "OR T J",
            "NOT C T",
            "OR T J",
            # check if can jump
            "AND D J",
        ]
        return self._run_spring_code(my_spring_script, 'WALK')

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        # Thought on Autogenerating a program:
        #   There are 11 read registers: A B C D E F G H I and T J 
        #   There are 2 write registers: T J
        #   There are 3 instructions: AND OR NOT
        #     each takes a read register and a write register
        #     22: 11*2 combinations per instruction
        #     66: Possible instructions
        #   Up to len 15:
        #     Len 0:    1 Program
        #     Len 1:   66 Programs
        #     Len 2: 4356 Programs
        #     ...
        #   In total ~ 2E27 programs possible
        #     so probably don't want to try and brute force
        #   (
        #     There are some optimizations available:
        #       * T AND T - NO-OP
        #       * T OR T - NO-OP
        #       * J AND J - NO-OP
        #       * J OR J - NO-OP
        #   )

        # Thought on autogenerating test cases
        #   There is only 2^9 (512) possible inputs
        #   It should be possible to define the desired behavior
        #     for all inputs
        #   And more quickly iterate?

        auto_determine_solution()