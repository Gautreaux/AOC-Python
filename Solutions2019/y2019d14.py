
from dataclasses import dataclass, field
import functools
from math import ceil
from typing import Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from AOC_Lib.DiscreteSearch import DiscreteSearch


@dataclass(frozen=True)
class Chemical:
    """A chemical in a reaction"""

    name: str

    consumed_by: set['Reaction'] = field(default_factory=set, hash=False)
    produced_by: set['Reaction'] = field(default_factory=set, hash=False)


@dataclass(frozen=True)
class Reaction:
    """A Reaction of chemicals"""

    reactants: frozenset[tuple[Chemical, int]]
    product: tuple[Chemical, int]


class Solution_2019_14(SolutionBase):
    """https://adventofcode.com/2019/day/14"""


    def _chemical_factory(self, name: str) -> Chemical:
        """Create/Cache chemicals"""
        if name in self._chemicals:
            return self._chemicals[name]
        else:
            c = Chemical(name)
            self._chemicals[name] = c
            return c

    def _parse_chemicals_and_qty(self, chemicals_and_qty: str) -> list[tuple[Chemical, int]]:
        """Parse a list of chemicals and quantity"""

        to_return: list[tuple[Chemical, int]] = []

        for s in chemicals_and_qty.split(','):
            s = s.strip()
            qty, name = s.split(" ")
            to_return.append((self._chemical_factory(name), int(qty)))
        return to_return


    def _ensure_dag(self) -> None:
        """Ensure the production graph is a Directed Acyclic Graph
        
        Raise a RuntimeError if it isn't
        """

        pending: set[Chemical] = set()

        def visit_node(c: Chemical):
            if c in pending:
                raise RuntimeError('Cycle Detected')
            pending.add(c)
            for r in c.consumed_by:
                visit_node(r.product[0])
            pending.remove(c)
        
        try:
            s = self._chemical_factory('ORE')
            visit_node(s)
        except RuntimeError as e:
            raise e from None

    def __post_init__(self):
        """Runs Once After `__init__`"""

        self._chemicals: dict[str, Chemical] = {}
        self._reactions: list[Reaction] = []

        for line in self.input_str_list(include_empty_lines=False):
            reactants_str, _, products_str = line.partition("=>")

            reactants = frozenset(self._parse_chemicals_and_qty(reactants_str))
            products = self._parse_chemicals_and_qty(products_str)

            assert len(products) == 1

            self._reactions.append(Reaction(reactants, products[0]))

        # Build the consumption and production graph

        for r in self._reactions:
            r.product[0].produced_by.add(r)
            for c in r.reactants:
                c[0].consumed_by.add(r)

        for c in self._chemicals.values():
            assert len(c.produced_by) <= 1

        # Ensure that the graph is DAG graph
        #   this makes things much easier later
        self._ensure_dag()

    @functools.cache
    def _get_minimum_ore_for_n_items(self, chemical: Chemical, qty: int) -> int:
        """Get the minimum amount of ore to produce `qty` of `chemical`"""
        
        if chemical.name == 'ORE':
            return qty
        
        assert len(chemical.produced_by) == 1
        reaction = next(iter(chemical.produced_by))

        # For when output is more than one
        multi_output_scale = reaction.product[1]

        return sum(map(
            lambda x: self._get_minimum_ore_for_n_items(
                x[0], ceil((x[1]*qty) / multi_output_scale)
            ),
            reaction.reactants,
        ))

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        return self._get_minimum_ore_for_n_items(
            self._chemical_factory('FUEL'), 1
        )

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        f = self._chemical_factory('FUEL')
        search = DiscreteSearch(
            lambda x: self._get_minimum_ore_for_n_items(f, x)
        )

        return search.find_biggest_less_than_equal_to(target=1000000000000)