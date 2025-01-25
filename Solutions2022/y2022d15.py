
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum, IntEnum, unique
from functools import reduce, cache
import itertools
from operator import mul
from typing import Any, Iterator, Type, TypeVar, Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from AOC_Lib.Geometry.DiscreteRegions import DiscreteAABBbounds
from AOC_Lib.Geometry.Point import DiscretePoint1, DiscretePoint2
from AOC_Lib.Geometry.PointTransforms import Direction2, DirectionsCharset_T


_DEFAULT_Y_TEST = 2000000

@dataclass(frozen=True)
class SensorBeaconPair:
    sensor_position: DiscretePoint2
    beacon_position: DiscretePoint2


    def generate_points_where_beacon_is_excluded(self, y_test: int = _DEFAULT_Y_TEST) -> Iterator[DiscretePoint2]:
        """Generate the set of points where the beacon cannot be"""

        sensor_dist_to_beacon = self.sensor_position.manhattan_distance(self.beacon_position)
        sensor_dist_to_y = self.sensor_position.manhattan_distance(DiscretePoint2(self.sensor_position.x, y_test))
        x_offset = sensor_dist_to_beacon - sensor_dist_to_y
        
        if x_offset == 0:
            # The beacon is on the Y_TEST
            #   no points cannot be the beacon
            return
        elif x_offset <= 0:
            # The sensor is further from the line
            #   than from its beacon
            # so no meaningful data can be inferred
            return

        for x in range(self.sensor_position.x-x_offset, self.sensor_position.x+x_offset+1):
            p = DiscretePoint2(x, _DEFAULT_Y_TEST)
            if p == self.beacon_position:
                continue
            yield p

    def get_aabb_where_beacon_is_excluded(self, y_test: int = _DEFAULT_Y_TEST) -> Iterator[DiscreteAABBbounds]:
        """Generate sets of bounds of all possible points"""

        sensor_dist_to_beacon = self.sensor_position.manhattan_distance(self.beacon_position)
        sensor_dist_to_y = self.sensor_position.manhattan_distance(DiscretePoint2(self.sensor_position.x, y_test))
        x_offset = sensor_dist_to_beacon - sensor_dist_to_y

        if x_offset == 0:
            # The beacon is on the Y_TEST
            #   no points cannot be the beacon
            return
        elif x_offset <= 0:
            # The sensor is further from the line
            #   than from its beacon
            # so no meaningful data can be inferred
            return

        x_min = self.sensor_position.x - x_offset
        x_max = self.sensor_position.x + x_offset

        if self.beacon_position.y != y_test:
            yield DiscreteAABBbounds(DiscretePoint1(x_min), DiscretePoint1(x_max))
        elif self.beacon_position.x == x_min and x_min != x_max:
            yield DiscreteAABBbounds(DiscretePoint1(x_min+1), DiscretePoint1(x_max))
        elif self.beacon_position.x == x_max and x_min != x_max:
            yield DiscreteAABBbounds(DiscretePoint1(x_min), DiscretePoint1(x_max-1))
        else:
            yield DiscreteAABBbounds(DiscretePoint1(x_min), DiscretePoint1(self.beacon_position.x - 1))
            yield DiscreteAABBbounds(DiscretePoint1(self.beacon_position.x + 1), DiscretePoint1(x_max))


class Solution_2022_15(SolutionBase):
    """https://adventofcode.com/2022/day/15"""

    def __post_init__(self):
        """Runs Once After `__init__`"""
        
        self.sensors_and_beacons: list[SensorBeaconPair] = []

        for line in self.input_str_list(include_empty_lines=False):
            line = line.replace("=", ' ').replace(',', '').replace(':', '').split(' ')
            x_s = int(line[3])
            y_s = int(line[5])
            b_x = int(line[-3])
            b_y = int(line[-1])

            self.sensors_and_beacons.append(SensorBeaconPair(DiscretePoint2(x_s, y_s), DiscretePoint2(b_x, b_y)))

    def _get_bounds_for_y(
        self, 
        y_test: int = _DEFAULT_Y_TEST,
        limit_region: Optional[DiscreteAABBbounds] = None
    ) -> set[DiscreteAABBbounds]:
        """Test a specific Y"""
        bounds: set[DiscreteAABBbounds] = set(
            itertools.chain.from_iterable(
                map(
                    lambda s: s.get_aabb_where_beacon_is_excluded(y_test),
                     self.sensors_and_beacons,
                )
            )
        )

        if limit_region:
            bounds = set(itertools.chain.from_iterable(
                map(
                    lambda r: limit_region.mask_intersection([r]),
                    bounds,
                )
            ))

        reduced = True

        while reduced:
            reduced = False

            if len(bounds) == 1:
                break

            for s in bounds:
                for tst in bounds:
                    if s == tst:
                        continue
                    if s.intersects(tst):
                        reduced = True
                        bounds.remove(tst)
                        bounds.remove(s)
                        bounds.add(s.combine(tst))
                        break
                if reduced:
                    break
        return bounds


    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        bounds = self._get_bounds_for_y(_DEFAULT_Y_TEST)

        return sum(map(lambda aabb: aabb.area(), bounds))

    def _generate_candidate_distress_coordinates(
        self, 
        y_test: int = _DEFAULT_Y_TEST,
        x_bounds: DiscreteAABBbounds = DiscreteAABBbounds(DiscretePoint1(0), DiscretePoint1(4000000)),
    ) -> Iterator[DiscretePoint2]:
        """Generate the candidates for distress coordinates"""

        raise NotImplementedError()



    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        for y in range(0, 4000000+1):

            if y % 100000 == 0:
                print("Y:", y)

            

            bounds = self._get_bounds_for_y(y)