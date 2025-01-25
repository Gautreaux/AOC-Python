from AOC_Lib.NeighborGenerator import neighborGeneratorFactory
from AOC_Lib.DisjointSets import DisjointSets
from dataclasses import dataclass
from string import digits
import itertools


@dataclass(frozen=True)
class PartNumber:
    root: tuple[int, int]
    value: int
    borders_symbol: str

    @staticmethod
    def find_root(grid: list[list[str]], start_x: int, start_y: int) -> tuple[int, int]:
        assert grid[start_y][start_x] in digits

        while start_x > 0:
            if grid[start_y][start_x - 1] in digits:
                start_x -= 1
            else:
                break

        return (start_x, start_y)

    @staticmethod
    def parse_total(grid: list[list[str]], start_x: int, start_y: int) -> int:
        assert grid[start_y][start_x] in digits

        total = 0

        while True:
            if start_x < len(grid[start_y]):
                if grid[start_y][start_x] in digits:
                    total = total * 10 + int(grid[start_y][start_x])
                    start_x += 1
                else:
                    break
            else:
                break
        
        return total


    @classmethod
    def check_location(cls, grid: list[list[str]], start_x: int, start_y: int) -> "PartNumber | None":
        """Check if a location has a part number"""
        c = grid[start_y][start_x]
        if c not in digits:
            return None
        
        root_x, root_y = cls.find_root(grid, start_x, start_y)
        total = cls.parse_total(grid, root_x, root_y)
        borders_symbol: str = ''

        seen: set[tuple[int, int]] = set()
        frontier = [(root_x, root_y)]

        n_factory = neighborGeneratorFactory(len(grid[0])-1, len(grid)-1, allow_diagonal=True)

        while frontier:
            p = frontier.pop()
            if p in seen:
                continue
            seen.add(p)
            c = grid[p[1]][p[0]]

            if c not in digits and c != '.':
                borders_symbol = borders_symbol + c
            if c not in digits:
                continue
            if p[1] != root_y:
                continue

            for neighbor in n_factory(*p):
                if neighbor not in seen:
                    frontier.append(neighbor)

        return PartNumber((root_x, root_y), total, borders_symbol)




def y2023d3(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2023/d3.txt"
    print("2023 day 3:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    # for single line inputs
    for c in lineList[-1]:
        pass

    ds = DisjointSets(itertools.product(range(len(lineList[0])), range(len(lineList))))

    assert lineList[0][0] == '.'

    gear_locations: list[tuple[int, int]] = []

    for y in range(len(lineList)):
        for x in range(len(lineList[0])):
            c = lineList[y][x]
            if c == '.':
                ds.union((x,y), (0,0))
            if c == '*':
                gear_locations.append((x,y))
            if c not in digits:
                continue
            if x > 0 and lineList[y][x-1] in digits:
                ds.union((x,y), (x-1,y))
            if x < len(lineList[0])-1 and lineList[y][x+1] in digits:
                ds.union((x,y), (x+1,y))

    print('(Approximate) Number of numbers', len(ds))
    
    seen_sets: set = set()
    numbers: dict[int, PartNumber] = {}

    for y in range(len(lineList)):
        for x in range(len(lineList[0])):
            h = ds.find((x,y))
            if h in seen_sets:
                continue
            seen_sets.add(h)

            ps = PartNumber.check_location(lineList, x, y)
            if ps is not None:
                numbers[h] = ps

    print('Loaded Qty Number of Numbers:', len(numbers))

    Part_1_Answer = sum(p.value for p in numbers.values() if p.borders_symbol)

    Part_2_Answer = 0

    neighbor_gen = neighborGeneratorFactory(len(lineList[0])-1, len(lineList)-1, allow_diagonal=True)

    for g in gear_locations:
        neighbors: dict[int, PartNumber] = {}
        for x,y in neighbor_gen(*g):
            if lineList[y][x] not in digits:
                continue
            h = ds.find((x,y))
            if h not in neighbors:
                neighbors[h] = numbers[h]
        
        assert len(neighbors) <= 2
        if len(neighbors) < 2:
            continue

        gen = iter(neighbors.values())
        Part_2_Answer += next(gen).value * next(gen).value

    return (Part_1_Answer, Part_2_Answer)