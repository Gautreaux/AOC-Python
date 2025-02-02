from dataclasses import dataclass, field
import itertools
from typing import Iterator, Optional
import re


from AOC_Lib.SolutionBase import SolutionBase, Answer_T


@dataclass
class Node:
    """A node in the map"""

    name: str
    left: "Node"
    right: "Node"


@dataclass
class PathTracker:
    """Track a node from a specific start position"""

    node: Node
    gen: Iterator[tuple[str, int]]
    prior: tuple[str, int] = field(init=False, default=("", -1))

    @property
    def prior_setp_count(self) -> int:
        """Return the current step count in prior"""
        return self.prior[1]

    def next_greater_equal_to(self, value: int) -> tuple[str, int]:
        """Get the next end state that is at a step count greater than or equal to the given value"""
        # This should definitely think about some cycle detection
        while self.prior[1] < value:
            self.prior = next(self.gen)
        return self.prior


class Solution_2023_08(SolutionBase):
    """https://adventofcode.com/2023/day/8"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        self.directions: str = self.input_str_list(include_empty_lines=False)[0]

        tokens: list[tuple[str, str, str]] = []

        # Split the line from the `XXX = (YYY, ZZZ)` format
        for line in self.input_str_list(include_empty_lines=False)[1:]:
            r = re.match(r"(\w+) = \((\w+), (\w+)\)", line)
            if r is None:
                raise RuntimeError(f"Invalid line: {line}")
            tokens.append((r.group(1), r.group(2), r.group(3)))

        empty_node: Node = Node("", object(), object())  # type: ignore
        nodes: dict[str, Node] = {}
        for t in tokens:
            for tt in t:
                if tt not in nodes:
                    nodes[tt] = Node(tt, empty_node, empty_node)

        for t in tokens:
            nodes[t[0]].left = nodes[t[1]]
            nodes[t[0]].right = nodes[t[2]]

        # Check that no nodes still reference the empty node
        for n in nodes.values():
            if n.left == empty_node or n.right == empty_node:
                raise RuntimeError(f"Node {n.name} still references the empty node")

        self.nodes: dict[str, Node] = nodes

    def generate_paths(self, start_pos: str) -> Iterator[tuple[str, int]]:
        """Generate tuples of ending pos (ends with `..Z`) and step count"""

        if start_pos.endswith("Z"):
            yield (start_pos, 0)

        current_pos: Node = self.nodes[start_pos]

        for i, s in enumerate(itertools.cycle(self.directions), start=1):
            if s == "L":
                current_pos = current_pos.left
            elif s == "R":
                current_pos = current_pos.right
            else:
                raise ValueError(f"Invalid direction {s}")

            if current_pos.name.endswith("Z"):
                yield (current_pos.name, i)

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        for n, i in self.generate_paths("AAA"):
            if n == "ZZZ":
                return i
        raise RuntimeError(
            '[Expect Unreachable] Stoped iterating paths before a soltion could be found!'
        )

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        # Needs some optimization (likely via Chinese Remainder Theorem)

        trackers: list[PathTracker] = []
        for n in self.nodes.values():
            if n.name.endswith("A"):
                trackers.append(PathTracker(n, self.generate_paths(n.name)))

        for t in trackers:
            t.next_greater_equal_to(0)

        while True:
            if all(
                (trackers[0].prior_setp_count == t.prior_setp_count for t in trackers)
            ):
                # All the step counts line up! Everyone on an end state
                return trackers[0].prior_setp_count

            # Advance all trackers to the next best step count
            mx = max(t.prior_setp_count for t in trackers)
            print("Advancing all trackers to", mx)
            for t in trackers:
                t.next_greater_equal_to(mx)
