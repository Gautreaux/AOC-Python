
from collections import deque
from dataclasses import dataclass, field
from typing import Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T


@dataclass
class Planet:
    """A Planet"""

    name: str
    
    orbiting: Optional['Planet'] = None

    moons: set['Planet'] = field(default_factory=set)

    _depth: int = field(default=-1, init=False, compare=False, hash=False)

    @property
    def depth(self) -> int:
        """The distance (orbital transfers) from `COM`. Also Number Orbits"""
        if self.orbiting is None:
            return 0
        if self._depth == -1:
            self._depth = self.orbiting.depth + 1 
        return self._depth

    def __hash__(self) -> int:
        return hash(self.name)


class Solution_2019_06(SolutionBase):
    """https://adventofcode.com/2019/day/6"""

    def _get_planet(self, name: str) -> Planet:
        try:
            return self.planets[name]
        except KeyError:
            p = Planet(name)
            self.planets[name] = p
            return p

    def __post_init__(self):
        """Runs Once After `__init__`"""
        
        self.planets: dict[str, Planet] = {}

        for r in self.input_str_list():
            base, _, moon = r.partition(')')  

            base_planet = self._get_planet(base)
            moon_planet = self._get_planet(moon)

            base_planet.moons.add(moon_planet)
            if moon_planet.orbiting is not None:
                raise RuntimeError
            else:
                moon_planet.orbiting = base_planet

        self.planets['COM']._depth = 0


    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        return sum(map(
            lambda p: p.depth,
            self.planets.values(),
        ))

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        target = self.planets['SAN'].orbiting
        assert target != None

        visited = set()
        frontier: deque[tuple[Planet, int]] = deque()
        frontier.append((self.planets['YOU'], 0))

        while frontier:
            (new_p, new_d) = frontier.popleft()

            if new_p.name == target.name:
                return new_d

            visited.add(new_p.name)

            if new_p.orbiting is not None and new_p.orbiting.name not in visited:
                frontier.append((new_p.orbiting, new_d + 1))
            
            for m in new_p.moons:
                if m.name not in visited:
                    frontier.append((m, new_d + 1))
