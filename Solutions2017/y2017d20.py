# from AOC_Lib.name import *

import itertools
from typing import Generator

ParticleVelocity_T = tuple[int, int, int]
ParticlePosition_T = tuple[int, int, int]
ParticleAcceleration_T = tuple[int, int, int]


class Particle:
    def __init__(
        self,
        p: ParticlePosition_T,
        v: ParticleVelocity_T,
        a: ParticleAcceleration_T,
        number: int = -1,
    ) -> None:
        self.p: ParticlePosition_T = p
        self.v: ParticleVelocity_T = v
        self.a: ParticleAcceleration_T = a
        self.number: int = number

    @property
    def delta_speed(self) -> int:
        """Return the "manhattan acceleration" of the particle"""
        return sum(map(abs, self.a))

    @property
    def start_speed(self) -> int:
        """Return the starting "manhattan speed" of the particle"""
        return sum(map(abs, self.v))

    @property
    def start_dist(self) -> int:
        """Return the starting manhattan distance of the particle"""
        return sum(map(abs, self.p))

    def positions(self) -> Generator[ParticlePosition_T, None, None]:
        """Return an infinite generator of particle position"""
        last_pos = self.p
        last_vel = self.v
        yield last_pos

        while True:
            last_vel = tuple(map(lambda x, y: x + y, last_vel, self.a))
            last_pos = tuple(map(lambda x, y: x + y, last_pos, last_vel))
            yield last_pos


def parseValues(s: str) -> tuple[int, int, int]:
    """Parse three int values from s"""
    s = s[3:-1].split(",")
    return tuple(map(int, s))


def parseParticle(s: str, number: int = -1) -> Particle:
    """Parse the particle values and return"""
    s = s.split(", ")
    return Particle(*map(parseValues, s), number=number)


def y2017d20(inputPath=None):
    if inputPath == None:
        inputPath = "Input2017/d20.txt"
    print("2017 day 20:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    particles = []

    for i, l in enumerate(lineList):
        particles.append(parseParticle(l, i))

    m_a = min(map(lambda x: x.delta_speed, particles))
    f = filter(lambda x: x.delta_speed == m_a, particles)
    l = list(f)
    m_s = min(map(lambda x: x.start_speed, l))
    f = filter(lambda x: x.start_speed == m_s, l)
    l = list(f)
    m_p = min(map(lambda x: x.start_dist, l))
    f = filter(lambda x: x.start_dist == m_p, l)
    l = list(f)
    assert len(l) == 1
    Part_1_Answer = l[0].number

    # Part 2

    # Particles can collide in a couple ways:
    #   1. just move into eachother
    #   2. Same velocity, different position, but different accel
    #   ....
    # Particles can never collide if:
    #   1. Same velocity and accel
    #   ...

    particles_and_positions = {x: x.positions() for x in particles}

    # TODO - this could be smarter, but it works
    #   at minimum can threshold on acceleration or velocity to know when to stop
    for i in range(10000):
        if i % 100 == 0:
            print(f"After {i} rounds, {len(particles_and_positions)} remain")
        new_pos = {}
        to_remove = set()

        for k, v in particles_and_positions.items():
            n = next(v)
            if n in new_pos:
                to_remove.add(k)
                to_remove.add(new_pos[n])
            else:
                new_pos[n] = k

        for r in to_remove:
            particles_and_positions.pop(r)

    Part_2_Answer = len(particles_and_positions)

    return (Part_1_Answer, Part_2_Answer)
