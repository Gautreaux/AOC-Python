# from AOC_Lib.name import *

from dataclasses import dataclass, field
import itertools
from typing import Callable, Optional


_DIMENSION_T = int
_POINT3_T = tuple[int, int, int]

@dataclass(frozen=True)
class NanoBot:

    position: _POINT3_T
    radius: int
    intersects_with: set['NanoBot'] = field(default_factory=set, hash=False, compare=False, init=False)

    @classmethod
    def from_input_line(cls, line: str) -> 'NanoBot':
        """Construct a nanobot from input"""
        p,r = line.split(" ")
        r_value = int(r[2:])
        p_value = tuple(map(int, p[5:-2].split(',')))
        return cls(p_value, r_value)

    def distance_to(self, other: 'NanoBot') -> int:
        """Return the distance between nanobots"""
        return sum(map(lambda x,y: abs(x-y), self.position, other.position))
 
    def distance_to_point(self, point: _POINT3_T) -> int:
        """Return the distance between this bot and a point"""
        return sum(map(lambda x,y: abs(x-y), self.position, point))

    def does_intersect(self, other: 'NanoBot') -> bool:
        """Return `True` iff the nanobot's ranges intersect at all"""
        return self.distance_to(other) <= (self.radius + other.radius)

    def contains(self, other: 'NanoBot') -> bool:
        """Return `True` iff `other` is inside this bot"""
        return self.distance_to(other) <= self.radius

    def contains_point(self, point: _POINT3_T) -> bool:
        """Return `True` iff the point is contained in this bot"""
        return self.distance_to_point(point) <= self.radius

    def check_set_intersection(self, other: 'NanoBot') -> bool:
        """Check if these two NanoBots intersect
            if so, update both `intersects_with` and return `True`
            else, return `False`
        """
        b = self.does_intersect(other)
        if b:
            self.intersects_with.add(other)
            other.intersects_with.add(self)
        return b

    @property
    def num_intersections(self) -> int:
        """Return number of intersections this has with others"""
        return len(self.intersects_with)

    def update_intersects(self, bot_filter: Callable[['NanoBot'], bool]) -> None:
        """Updates the intersects with to contain only those passing the filter"""
        new_set = set(filter(bot_filter, self.intersects_with))
        super().__setattr__('intersects_with', new_set)


@dataclass(frozen=True)
class _SearchParams:

    guess_lower_bound: int
    guess_upper_bound: int

    nanobots: set[NanoBot] = field(default_factory=set, hash=False, compare=False)

    def __post_init__(self):
        assert self.guess_lower_bound <= self.guess_upper_bound

    @property
    def answer(self) -> Optional[int]:
        """Return the answer (if we have one) or else `None`"""
        if self.guess_lower_bound == self.guess_upper_bound:
            return self.guess_lower_bound
        return None

    @property
    def guess_range(self) -> int:
        """Return the spread in guesses"""
        return self.guess_upper_bound - self.guess_lower_bound

    @property
    def aabb_volume(self) -> int:
        """Return the volume of the Axis Aligned Bounding Box of these nanobots"""
        min_x = min(map(lambda x: x.position[0], self.nanobots))
        min_y = min(map(lambda x: x.position[1], self.nanobots))
        min_z = min(map(lambda x: x.position[2], self.nanobots))
        max_x = max(map(lambda x: x.position[0], self.nanobots))
        max_y = max(map(lambda x: x.position[1], self.nanobots))
        max_z = max(map(lambda x: x.position[2], self.nanobots))
        return (max_x - min_x) * (max_y - min_y) * (max_z - min_z)

    def __str__(self) -> str:
        return "Range {:>04} [{:>04}-{:>04}] | {:>04} Nanobots Remain | Volume {}".format(
            self.guess_range, self.guess_lower_bound, self.guess_upper_bound,
            len(self.nanobots), self.aabb_volume,
        )

    def _prune_adjency(self) -> str:
        """Prune the adjency lists"""
        bot_filter = lambda x: x in self.nanobots

        for bot in self.nanobots:
            bot.update_intersects(bot_filter=bot_filter)
    
    def refine(self) -> '_SearchParams':
        """Refine to try and get a better guess"""
        if len(self.nanobots) < self.guess_upper_bound:
            return _SearchParams(
                guess_lower_bound=self.guess_lower_bound,
                guess_upper_bound=len(self.nanobots),
                nanobots=self.nanobots
            )

        to_return = self._refine()

        if to_return.nanobots != self.nanobots:
            # Some nanobot pruning occurred. 
            # Reset the adjency
            to_return._prune_adjency()
        
        return to_return

    def _reduce_largest_intersections(self) -> Optional['_SearchParams']:
        """Clamp max to the largest of mutual intersections"""
        max_cardinality_bot = max(self.nanobots, key=lambda x: len(x.intersects_with))
        max_c = len(max_cardinality_bot.intersects_with)

        if max_c < self.guess_upper_bound:
            return _SearchParams(
                guess_lower_bound=self.guess_lower_bound,
                guess_upper_bound=max_c,
                nanobots=self.nanobots,
            )
        return None

    def _get_count_at_pos_average(self) -> Optional['_SearchParams']:
        """Get the count at the position average of all bots"""

        # todo really want to check all eight points around here
        avg_point: _POINT3_T = tuple(map(
            lambda dimension: (
                sum(map(lambda nb: nb.position[dimension], self.nanobots)) // len(self.nanobots)
            ),
            range(3),
        ))
        
        # count all the bots that touch the average point
        # Ultimately, we need to find a clique of at least this size
        count_intersecting = sum(1 for _ in filter(lambda x: x.contains_point(avg_point), self.nanobots))

        # filter to nanobots with at least that many intersections
        new_nanobots = set(filter(
            lambda x: len(x.intersects_with) >= count_intersecting,
            self.nanobots,
        ))

        if count_intersecting > self.guess_lower_bound:
            return _SearchParams(
                guess_lower_bound=count_intersecting,
                guess_upper_bound=self.guess_upper_bound,
                nanobots=new_nanobots
            )
        return None
    
    def _refine(self) -> '_SearchParams':
        """Worker for `refine`"""

        t = self._reduce_largest_intersections()
        if t is not None:
            return t

        t = self._get_count_at_pos_average()
        if t is not None:
            return t

        return self



def y2018d23(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2018/d23.txt"
    print("2018 day 23:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    nanobots = list(map(NanoBot.from_input_line, lineList))

    strongest_nanobot = max(nanobots, key=lambda x: x.radius)

    Part_1_Answer = sum(1 for _ in filter(lambda x: strongest_nanobot.contains(x), nanobots))

    # Part_2

    # Rectilinear bounding box - lowest point
    bb_lower_point = tuple(map(lambda x: min(map(lambda y: y.position[x], nanobots)), range(3)))

    # Rectilinear bounding box - upper point
    bb_upper_point = tuple(map(lambda x: max(map(lambda y: y.position[x], nanobots)), range(3)))

    # Dimensional range of the bb
    bb_ranges = tuple(map(lambda x,y: x-y, bb_upper_point, bb_lower_point))

    print(f"{bb_ranges} -> {bb_ranges[0]*bb_ranges[1]*bb_ranges[2]}")


    # O(n^2) / 2
    for a,b in itertools.combinations(nanobots, 2):
        a.check_set_intersection(b)

    bot_touching_most = max(nanobots, key=lambda x: x.num_intersections)

    # Now all we need to do is find the Maximal Clique
    #   thats only NP-Complete so not too bad

    print(f"The bot touching most others touches {bot_touching_most.num_intersections}: {bot_touching_most.radius}")

    sp = _SearchParams(guess_lower_bound=0, guess_upper_bound=len(nanobots), nanobots=nanobots)

    for i in range(40):
        if i % 1 == 0:
            print(f"{i:>05} {str(sp)}")
        
        ans = sp.answer
        if ans is not None:
            Part_2_Answer = ans
            break

        sp = sp.refine()


    if Part_2_Answer is None:
        print("Too many cycles, terminating") 
    
    return (Part_1_Answer, Part_2_Answer)