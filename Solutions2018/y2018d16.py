# from AOC_Lib.name import *


from collections import Counter, namedtuple
from copy import copy
import itertools
from typing import Any, Callable, Generator, Iterator

from AOC_Lib.PartitionIterator import PartitionIterator

from operator import add, mul, and_, or_


Memory_T = list[int, int, int, int]
Instruction_T = namedtuple("Instruction_T", "op A B C")
ChangeSet_T = namedtuple("ChangeSet_T", "before instr after")
OP_T = Callable[[Memory_T, Instruction_T], Memory_T]


def generateThreeLineTuples(
    iterator: Iterator[Any],
) -> Generator[tuple[Any, Any, Any], None, None]:
    """Yield three line tuples of the iterator, raising a runtime error if the iterator len is not a 3 multiple"""
    while True:
        try:
            a = next(iterator)
        except StopIteration:
            return
        b = next(iterator)
        c = next(iterator)
        yield (a, b, c)


def parseChangeSet(before: str, instr: str, after: str) -> ChangeSet_T:
    """Parse the change set and return a tuple of tuples"""

    assert before.startswith("Before: [")
    before_mem = list(map(int, before.partition("Before: [")[-1][:-1].split(", ")))

    instr_t = Instruction_T(*map(int, instr.split()))

    assert after.startswith("After:  [")
    after_mem = list(map(int, after.partition("After:  [")[-1][:-1].split(", ")))

    return ChangeSet_T(before_mem, instr_t, after_mem)


def _op_r_common(
    mem: Memory_T, inst: Instruction_T, reduce: Callable[[int, int], int]
) -> Memory_T:
    """Common logic for all op_r"""
    mem[inst.C] = reduce(mem[inst.A], mem[inst.B])
    return mem


def _op_i_common(
    mem: Memory_T, inst: Instruction_T, reduce: Callable[[int, int], int]
) -> Memory_T:
    """Common logic for all op_i"""
    mem[inst.C] = reduce(mem[inst.A], inst.B)
    return mem


def op_addr(mem: Memory_T, inst: Instruction_T) -> Memory_T:
    """Add registers"""
    return _op_r_common(mem, inst, add)


def op_addi(mem: Memory_T, inst: Instruction_T) -> Memory_T:
    """Add immediate"""
    return _op_i_common(mem, inst, add)


def op_mulr(mem: Memory_T, inst: Instruction_T) -> Memory_T:
    """Multiply register"""
    return _op_r_common(mem, inst, mul)


def op_muli(mem: Memory_T, inst: Instruction_T) -> Memory_T:
    """Multiply immediate"""
    return _op_i_common(mem, inst, mul)


def op_banr(mem: Memory_T, inst: Instruction_T) -> Memory_T:
    """Bitwise AND register"""
    return _op_r_common(mem, inst, and_)


def op_bani(mem: Memory_T, inst: Instruction_T) -> Memory_T:
    """Bitwise AND immediate"""
    return _op_i_common(mem, inst, and_)


def op_borr(mem: Memory_T, inst: Instruction_T) -> Memory_T:
    """Bitwise OR register"""
    return _op_r_common(mem, inst, or_)


def op_bori(mem: Memory_T, inst: Instruction_T) -> Memory_T:
    """Bitwise OR immediate"""
    return _op_i_common(mem, inst, or_)


def op_setr(mem: Memory_T, inst: Instruction_T) -> Memory_T:
    """(set register) copies the contents of register A into register C. (Input B is ignored.)"""
    mem[inst.C] = mem[inst.A]
    return mem


def op_seti(mem: Memory_T, inst: Instruction_T) -> Memory_T:
    """(set immediate) stores value A into register C. (Input B is ignored.)"""
    mem[inst.C] = inst.A
    return mem


def op_gtir(mem: Memory_T, inst: Instruction_T) -> Memory_T:
    """greater-than immediate/register"""
    mem[inst.C] = 1 if inst.A > mem[inst.B] else 0
    return mem


def op_gtri(mem: Memory_T, inst: Instruction_T) -> Memory_T:
    """greater-than register/immediate"""
    mem[inst.C] = 1 if mem[inst.A] > inst.B else 0
    return mem


def op_gtrr(mem: Memory_T, inst: Instruction_T) -> Memory_T:
    """greater-than register/immediate"""
    mem[inst.C] = 1 if mem[inst.A] > mem[inst.B] else 0
    return mem


def op_eqir(mem: Memory_T, inst: Instruction_T) -> Memory_T:
    """equal immediate/register"""
    mem[inst.C] = 1 if inst.A == mem[inst.B] else 0
    return mem


def op_eqri(mem: Memory_T, inst: Instruction_T) -> Memory_T:
    """equal register/immediate"""
    mem[inst.C] = 1 if mem[inst.A] == inst.B else 0
    return mem


def op_eqrr(mem: Memory_T, inst: Instruction_T) -> Memory_T:
    """equal register/immediate"""
    mem[inst.C] = 1 if mem[inst.A] == mem[inst.B] else 0
    return mem


operators: list[OP_T] = [
    op_addr,
    op_addi,
    op_mulr,
    op_muli,
    op_banr,
    op_bani,
    op_borr,
    op_bori,
    op_setr,
    op_seti,
    op_gtir,
    op_gtri,
    op_gtrr,
    op_eqir,
    op_eqri,
    op_eqrr,
]


def getCandidatesForChange(change: ChangeSet_T) -> list[OP_T]:
    """Return a list of possible candidate for this change"""

    candidates = []
    for op in operators:
        res = op(copy(change.before), change.instr)
        if res == change.after:
            candidates.append(op)
    return candidates


def y2018d16(inputPath=None):
    if inputPath == None:
        inputPath = "Input2018/d16.txt"
    print("2018 day 16:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    change_sets_lns, test_program_lns = PartitionIterator(iter(lineList), ("", "", ""))
    change_sets_f = filter(lambda x: x != "", change_sets_lns)
    change_sets_r = generateThreeLineTuples(change_sets_f)
    change_sets = list(map(lambda x: parseChangeSet(*x), change_sets_r))

    Part_1_Answer = sum(
        1
        for _ in filter(
            lambda x: len(x) >= 3,
            map(getCandidatesForChange, change_sets),
        )
    )

    # Part 2

    op_code_possible_values: dict[int, set[OP_T]] = {
        k: set(operators) for k in range(len(operators))
    }

    for change in change_sets:
        op_options = getCandidatesForChange(change)
        s = set(op_options)
        op_code_possible_values[change.instr.op].intersection_update(s)

    op_code_values: dict[int, OP_T] = {}

    while len(op_code_values) < len(op_code_possible_values):

        op_code = None
        op = None

        if any(map(lambda x: len(x) == 1, op_code_possible_values.values())):
            # We can assign based on a code with only one candidate
            op_code, op_s = next(
                itertools.dropwhile(
                    lambda x: len(x[1]) != 1, op_code_possible_values.items()
                )
            )
            assert len(op_s) == 1
            op = next(iter(op_s))
            print(f"OP Code {op_code} has only {op}")
        elif any(
            map(
                lambda x: x == 1,
                (
                    c := Counter(
                        itertools.chain.from_iterable(op_code_possible_values.values())
                    )
                ).values(),
            )
        ):
            # We can assign based on a code in only one candidate
            # Turns out this isn't necessary if your <code with one candidate>
            #  is bug free
            # But it should work, so im leaving it
            op, _ = next(itertools.dropwhile(lambda x: x[1] != 1, c.items()))

            # now find the candidate for OP
            op_code, _ = next(
                itertools.dropwhile(
                    lambda x: x[1] != op,
                    itertools.chain.from_iterable(
                        map(
                            lambda y: zip(itertools.repeat(y[0]), iter(y[1])),
                            op_code_possible_values.items(),
                        ),
                    ),
                )
            )
            print(f"OP {op} appears in only candidate: {op_code}")
        else:
            print(op_code_possible_values)
            print(f"There is not a (trivial) unique solution")
            print(f"  A more complex solution _may_ exist")
            print(
                "  The unknown op_codes each have n candidates:",
                list(map(len, op_code_possible_values.values())),
            )
            print(
                "  The functions each appear n times: ",
                Counter(
                    itertools.chain.from_iterable(op_code_possible_values.values())
                ),
            )
            print("  The assigned op_codes are", op_code_values)
            # it is possible to construct the sets so as a solution is inferred
            #   but going to hope that this condition never arises
            raise

        assert op_code is not None
        assert op is not None
        assert op_code not in op_code_values
        assert op not in op_code_values.values()
        op_code_values[op_code] = op

        for v in op_code_possible_values.values():
            if op in v:
                v.remove(op)

    # now run program

    # convert lines to instruction format
    test_program = map(
        lambda x: Instruction_T(*map(int, x.split(" "))), test_program_lns
    )

    mem: Memory_T = [0, 0, 0, 0]

    for instr in test_program:
        op_code_values[instr.op](mem, instr)

    Part_2_Answer = mem[0]

    return (Part_1_Answer, Part_2_Answer)
