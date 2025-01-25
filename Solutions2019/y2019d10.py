
from collections import defaultdict
import itertools
import math
from typing import Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from AOC_Lib.Geometry.Point import DiscretePoint2, Point2


Ray2_T = Point2


def get_ray(a: DiscretePoint2, b: DiscretePoint2) -> Ray2_T:
    """Get the ray from a to b"""
    assert isinstance(a, DiscretePoint2)
    assert isinstance(b, DiscretePoint2)
    r = b-a
    ray = r.scale(1 / r.distance(DiscretePoint2(0,0)))
    return Point2(round(ray.x, 10), round(ray.y, 10))


class Solution_2019_10(SolutionBase):
    """https://adventofcode.com/2019/day/10"""

    def __post_init__(self):
        """Runs Once After `__init__`"""
        
        self.asteroid_positions: list[DiscretePoint2] = []

        for y, line in enumerate(self.input_str_list(include_empty_lines=False)):
            for x, char in enumerate(line):
                if char == '#':
                    self.asteroid_positions.append(DiscretePoint2(x,y))

    def get_visible_directions(self, origin: DiscretePoint2) -> set[Ray2_T]:
        """Get all asteroids visible from the origin"""
        
        rays: set[Ray2_T] = set()

        for other_asteroid in self.asteroid_positions:
            if other_asteroid == origin:
                continue

            rays.add(get_ray(origin, other_asteroid))
        return rays

    def get_asteroid_most_visible(self) -> DiscretePoint2:
        """Return the position of the asteroid that can see the most"""

        asteroids_and_qty_seen = map(lambda x: (x, len(self.get_visible_directions(x))), self.asteroid_positions)
        best_asteroid_and_qty = max(asteroids_and_qty_seen, key=lambda x: x[1])
        return best_asteroid_and_qty[0]

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        return max(map(lambda x: len(self.get_visible_directions(x)), self.asteroid_positions))

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        base_asteroid = self.get_asteroid_most_visible()

        print("Base Asteroid is on: {}".format(base_asteroid))


        # Build a mapping of rays to the asteroids
        to_vaporize_dict: defaultdict[Ray2_T, list[DiscretePoint2]] = defaultdict(list)
        for a in self.asteroid_positions:
            if a == base_asteroid:
                continue
            to_vaporize_dict[get_ray(base_asteroid, a)].append(a)

        # Convert the ray to its corresponding angle with the X-Axis in radians
        to_vaporize_angle: list[tuple[float, list[DiscretePoint2]]] = list(map(
            lambda rt: (math.atan2(rt[0].y, rt[0].x), rt[1]),
            to_vaporize_dict.items(),
        ))

        # organize in reverse 'destruction order'
        #   i.e. how close they are to the base
        # Note: we want to use the list like a stack
        #   so we place the furthest away items first (reverse sort)
        for _,aligned_asteroids in to_vaporize_angle:
            if len(aligned_asteroids) == 0:
                continue
            aligned_asteroids.sort(key=lambda x: base_asteroid.distance(x), reverse=True)

        # Sort the rays
        #   based on their angle (in radians) with the positive x axis
        # There is some coordinate system nastiness that all cancels out:
        #  * The laser moves clockwise
        #  * The laser starts "up"
        #  * Positive Y is "down"
        # The first and last point cancel each other out
        #   and increasing radians is the same as the direction of the laser travel
        #   we just need to keep in mind that the start point ("up") is at -pi/2
        #       which is non-standard
        to_vaporize_angle.sort()

        # Iterator to cycle over the asteroids forever
        i = itertools.cycle(to_vaporize_angle)

        # Skip the first portion since laser starts point "upwards"
        #   awful coordinate system stuff
        i = itertools.dropwhile(lambda x: x[0] < -math.pi / 2, i)

        last_pop = None
        destroyed_200th = None
        ctr = 0
        for _, asteroids in i:

            # vaporize the closest asteroid along this angle
            if asteroids:
                last_pop = asteroids.pop()
                ctr += 1
                if ctr == 200:
                    destroyed_200th = last_pop
                # print(f"{ctr:>03} Destroyed {last_pop} <{last_pop-base_asteroid}> {round(_, 4)} {base_asteroid.distance(last_pop)}")

                # check if there are any asteroids left
                if not any(map(lambda x: x[1], to_vaporize_angle)):
                    break
        if destroyed_200th is None:
            raise RuntimeError('???')

        return destroyed_200th.x * 100 + destroyed_200th.y
