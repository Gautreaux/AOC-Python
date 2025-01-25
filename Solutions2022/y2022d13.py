
from functools import cmp_to_key
import itertools
from typing import Iterator,  Optional, Union

from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from AOC_Lib.SlidingWindow import batched


Packet_T = list[Union['Packet_T', int]]


def _is_in_proper_order(lhs: Packet_T, rhs: Packet_T):
    """cmp style comparison:
    
    -1: lhs < rhs
     0: lhs = rhs
     1: lhs > rhs
    """

    assert isinstance(lhs, list)
    assert isinstance(rhs, list)

    for x,y in zip(lhs,rhs):

        assert isinstance(x, int) or isinstance(x, list)
        assert isinstance(y, int) or isinstance(y, list)

        x_is_int = isinstance(x, int)
        y_is_int = isinstance(y, int)

        if x_is_int and y_is_int:
            if x < y:
                return -1
            elif x > y:
                return 1
            else:
                continue
        elif not x_is_int and not y_is_int:
            r = _is_in_proper_order(x, y) # type: ignore
        else:
            u = [x] if x_is_int else x
            v = [y] if y_is_int else y
            r = _is_in_proper_order(u,v) # type: ignore

        if r != 0:
            return r
        else:
            continue

    if len(lhs) < len(rhs):
        return -1
    elif len(lhs) > len(rhs):
        return 1
    else:
        return 0


def _parse(i : Iterator[str], d: int = 0) -> Packet_T:
    """Parse a packet out of the stream"""
    this_list = []

    pool = []

    while True:
        try:
            n = next(i)
        except StopIteration:
            if d == 0:
                return this_list[0]
            else:
                raise

        if n == '[':
            this_list.append(_parse(i, d+1))
        elif n == ']' or n == ',':
            if pool:
                this_list.append(int("".join(pool)))
                pool = []
            if n == ']':
                return this_list
        elif n in '0123456789':
            pool.append(n)
        else:
            raise RuntimeError(n)


class Solution_2022_13(SolutionBase):
    """https://adventofcode.com/2022/day/13"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        self.packet_pairs: list[tuple[Packet_T, Packet_T]] = []

        for a,b in batched(self.input_str_list(include_empty_lines=False), 2):
            try:
                ap = _parse(iter(a))
                bp = _parse(iter(b))
                self.packet_pairs.append((ap, bp))
            except:
                print(a)
                print(b)
                raise

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        ctr = 0

        for i,(lhs, rhs) in enumerate(self.packet_pairs, 1):
            if _is_in_proper_order(lhs, rhs) == -1:
                ctr += i
        return ctr


    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        all_packets = list(itertools.chain.from_iterable(self.packet_pairs))

        decoder_a: Packet_T = [[2]]
        decoder_b: Packet_T = [[6]]
        all_packets.append(decoder_a)
        all_packets.append(decoder_b)

        all_packets.sort(key=cmp_to_key(_is_in_proper_order))

        dec_a_index = all_packets.index(decoder_a) + 1
        dec_b_index = all_packets.index(decoder_b) + 1

        return dec_a_index * dec_b_index


