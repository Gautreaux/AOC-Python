from dataclasses import dataclass
import itertools
from math import lcm
from typing import Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from AOC_Lib.Geometry.Point import DiscretePoint3


@dataclass
class Moon:
    """A moon with position and velocity"""

    position: DiscretePoint3
    velocity: DiscretePoint3

    @property
    def potential_energy(self) -> int:
        """The moon's potential energy"""
        return sum(map(abs, self.position))

    @property
    def kinetic_energy(self) -> int:
        """The moon's kinetic energy"""
        return sum(map(abs, self.velocity))

    @property
    def total_energy(self) -> int:
        """The moon't total energy"""
        return self.potential_energy * self.kinetic_energy

    def apply_gravity(self, other: "Moon") -> None:
        """Apply the gravity to BOTH moons"""

        modifiers = map(
            lambda a, b: ((1, -1) if a < b else ((0, 0) if a == b else (-1, 1))),
            self.position,
            other.position,
        )

        m1, m2 = itertools.tee(modifiers, 2)

        self.velocity += DiscretePoint3(*map(lambda x: x[0], m1))
        other.velocity += DiscretePoint3(*map(lambda x: x[1], m2))

    def apply_velocity(self) -> None:
        """Update position based on current velocity"""
        self.position += self.velocity


class Solution_2019_12(SolutionBase):
    """https://adventofcode.com/2019/day/12"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        self.moons: list[Moon] = []
        self.starting_positions: list[DiscretePoint3] = []

        for line in self.input_str_list(include_empty_lines=False):
            positions = map(
                lambda x: int(x.strip().partition("=")[-1]),
                line[1:-1].split(","),
            )
            self.moons.append(
                Moon(
                    position=DiscretePoint3(*positions),
                    velocity=DiscretePoint3(0, 0, 0),
                )
            )
            self.starting_positions.append(self.moons[-1].position)

    def _simulate_one_step(self):
        """Advance the simulation by one step"""

        for a, b in itertools.combinations(self.moons, 2):
            a.apply_gravity(b)
        for m in self.moons:
            m.apply_velocity()

    def _get_one_dimensional_period(
        self, positions: list[int], starting_velocity: int = 0
    ) -> int:
        """Get the period across one dimension"""

        # copy
        positions = list(positions)
        velocities = [starting_velocity] * len(positions)

        # mapping configs to when they occurred
        seen_configs = {}

        for i in itertools.count():

            # Check and update seen configurations
            this_config = tuple(itertools.chain(positions, velocities))
            if this_config in seen_configs:
                past = seen_configs[this_config]
                return i - past
            else:
                seen_configs[this_config] = i

            # Now update velocity
            for i in range(len(positions)):
                for j in range(len(positions)):
                    if positions[i] == positions[j]:
                        continue
                    elif positions[i] < positions[j]:
                        velocities[i] += 1
                    else:
                        velocities[i] -= 1

            # Update positions
            for i in range(len(positions)):
                positions[i] += velocities[i]

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        for _ in range(1000):
            self._simulate_one_step()
        return sum(map(lambda x: x.total_energy, self.moons))

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        # Each dimension is independent
        #   so find when each dimension repeats,
        #   and then find the LCM of that

        periods: list[int] = []

        # [186028, 84032, 286332]

        for dim in range(3):
            start_positions = list(
                map(
                    lambda x: x[dim],
                    self.starting_positions,
                )
            )
            periods.append(self._get_one_dimensional_period(start_positions))

        print(f"Resolved periods: {periods}")

        return lcm(*periods)
