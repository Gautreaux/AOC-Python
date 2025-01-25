from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum, IntEnum, unique
from functools import reduce, cache
import itertools
from math import lcm
from operator import mul, add
from typing import Any, Callable, Iterator, Type, TypeVar, Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from AOC_Lib.Geometry.Point import DiscretePoint2


@dataclass
class Monkey:

    monkey_id: int
    items: list[int] = field(default_factory=list)
    operation: Callable[[int], int] = lambda x: x
    divisor: int = 0
    on_true: Optional["Monkey"] = None
    on_false: Optional["Monkey"] = None

    _number_inspections: int = 0

    def take_turn(self, worry_action: Callable[[int], int]) -> None:
        """Take a single turn (throw all items)"""

        assert self.on_false is not None
        assert self.on_true is not None

        # print(f"Monkey {self.monkey_id}:")

        old_items = self.items
        self.items = []
        for i in old_items:

            # print(f"  Inspect Level: {i}")

            self._number_inspections += 1
            new_worry = self.operation(i)
            # print(f"    op Level: {new_worry}")
            new_worry = worry_action(new_worry)
            # print(f"    Bored Level: {new_worry}")
            if new_worry % self.divisor == 0:
                # print(f"    is divis")
                # print(f"    Throw {new_worry} to {self.on_true.monkey_id}")
                self.on_true._receive_item(new_worry)
            else:
                # print(f"    is not divis")
                # print(f"    Throw {new_worry} to {self.on_false.monkey_id}")
                self.on_false._receive_item(new_worry)

    def _receive_item(self, item: int) -> None:
        self.items.append(item)


class Solution_2022_11(SolutionBase):
    """https://adventofcode.com/2022/day/11"""

    def _ensure_monkey(self, mk_id: int) -> Monkey:
        try:
            return self._monkeys[mk_id]
        except KeyError:
            m = Monkey(mk_id)
            self._monkeys[mk_id] = m
            return m

    def _iter_monkeys(self) -> Iterator[Monkey]:
        """Iterate the monkeys in increasing id order"""
        ids = list(self._monkeys.keys())
        ids.sort()
        for i in ids:
            yield self._monkeys[i]

    def _parse_monkeys(self):

        self._monkeys: dict[int, Monkey] = {}

        itr = iter(self.input_str_list(include_empty_lines=True))

        while True:
            this_lines = list(itertools.takewhile(lambda x: len(x) > 0, itr))
            if not this_lines:
                break
            assert len(this_lines) == 6

            mk_id = int(this_lines[0].split(" ")[-1][:-1])

            monkey = self._ensure_monkey(mk_id)

            monkey.items.extend(map(int, this_lines[1].replace(",", "").split(" ")[2:]))

            s = this_lines[2].split(" ")
            assert s[1] == "new"
            assert s[2] == "="
            assert s[3] == "old"
            operator = s[-2]
            operand = s[-1]

            if operator == "*":
                op = mul
            elif operator == "+":
                op = add
            else:
                raise NotImplementedError(operator)

            if operand == "old":
                monkey.operation = (lambda op_: (lambda x: op_(x, x)))(op)
            else:
                operand_int = int(operand)
                monkey.operation = (lambda op_, oi: (lambda x: op_(x, oi)))(
                    op, operand_int
                )

            s = this_lines[3].split(" ")
            assert s[1] == "divisible"
            assert s[2] == "by"
            operand_int = int(s[3])
            monkey.divisor = operand_int

            s = this_lines[4].split(" ")
            assert s[1] == "true:"
            monkey.on_true = self._ensure_monkey(int(s[-1]))
            s = this_lines[5].split(" ")
            assert s[1] == "false:"
            monkey.on_false = self._ensure_monkey(int(s[-1]))

        for m in self._monkeys.values():
            assert m.on_false is not None
            assert m.on_true is not None
            assert m.divisor != 0

    def _run_round(self, worry_modifier: Callable[[int], int]):
        for m in self._iter_monkeys():
            m.take_turn(worry_modifier)

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        self._parse_monkeys()

        def worry_modifier(x):
            return x // 3

        for _ in range(20):
            self._run_round(worry_modifier)

        return max(
            map(
                lambda t: t[0]._number_inspections * t[1]._number_inspections,
                itertools.combinations(self._iter_monkeys(), 2),
            )
        )

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        self._parse_monkeys()
        lcm_ = lcm(*map(lambda x: x.divisor, self._iter_monkeys()))

        def worry_modifier(x):
            return x % lcm_

        for i in range(10000):
            if i % 500 == 0:
                print("I =", i)
            self._run_round(worry_modifier)

        return max(
            map(
                lambda t: t[0]._number_inspections * t[1]._number_inspections,
                itertools.combinations(self._iter_monkeys(), 2),
            )
        )
