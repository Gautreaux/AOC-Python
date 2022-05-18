# from AOC_Lib.name import *

from collections import deque
import functools
import itertools
from typing import Generator, Iterable


ALL_DIST_LIMIT = 10000


def generateManhattanNeighbors(
    start_xy: tuple[int, int], 
) -> Generator[tuple[int, int], None, None]:
    """Return all the manhattan distance neighbors of the point
        points are ordered in increasing depth and otherwise unordered
    """

    transforms = [
        ( 0,  1),
        ( 0, -1),
        ( 1,  0),
        (-1,  0),
    ]

    for f in map(
        lambda x: tuple(
            map(
                lambda y,z: y+z, 
                x, start_xy,
            )
        ),
        transforms,
    ):
        yield f


def generateManhattanNeighborsIncreasing(
    start_xy: tuple[int, int],
) -> Generator[Iterable[tuple[int, int]], None, None]:
    """Generate successive iterators of successive manhattan distance
        ex: the first iterable will be just the point
            the second iterable will be all adjacent points (manhattan distance 1)
            the third iterable will be all points at manhattan distance 2
            ....
        points within each iterable are unordered
    """

    # the first iterable
    yield [start_xy]

    last_points = [start_xy]

    for i in itertools.count(1):
        new_points = set(filter(
            lambda x: manhattanDist(x, start_xy) == i,
            itertools.chain.from_iterable(
                map(generateManhattanNeighbors, last_points)
            ),
        ))
        yield iter(new_points)
        last_points = new_points


def manhattanDist(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Return the manhattan distance between the two points"""
    return sum(map(lambda u,v: abs(u-v), a, b))


def getAllDistScore(test_point: tuple[int, int], points_list: list[tuple[int, int]]) -> int:
    """Returns the sum of manhattan distances from test_point to all elements of points_list"""
    return sum(map(lambda x: manhattanDist(test_point, x), points_list))


def y2018d6(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2018/d6.txt"
    print("2018 day 6:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    points = list(map(lambda x: tuple(map(int, x.split(", "))), lineList))

    min_x = min(map(lambda x: x[0], points))
    min_y = min(map(lambda x: x[1], points))

    # transform so that things are left and top aligned
    #   not sure this was necessary but whatever
    points = list(map(lambda x: (x[0] - min_x, x[1] - min_y), points))

    min_x = min(map(lambda x: x[0], points))
    min_y = min(map(lambda x: x[1], points))
    max_x = max(map(lambda x: x[0], points))
    max_y = max(map(lambda x: x[1], points))
    num_points = len(points)

    assert(min_x == 0)
    assert(min_y == 0)

    print("There are {} points in the X span {}-{} ({}) and Y span {}-{} ({}). PEM: ({})".format(
        num_points, min_x, max_x, max_x - min_x + 1,
        min_y, max_y, max_y - min_y + 1, 
        num_points * (max_x - min_x + 1) * (max_y - min_y + 1)
    ))

    ### Part 1

    generators = list(map(generateManhattanNeighborsIncreasing, points))
    results = [0]*num_points
    done_map = [False]*num_points
    is_inf = [False]*num_points

    visited_points = set()

    for i in range(max(max_x, max_y)):
        if all(done_map):
            break

        print(f"Starting points at distance {i}")

        new_frontiers = []

        # get the frontiers for each object
        for g in generators:
            # we need to keep calculating the sets so that
            #   things on the edge properly claim space in the center
            #   remove the visited so that we only get new furthest points
            s = set(next(g))
            new_frontiers.append(s - visited_points)

        # update visited
        for p in itertools.chain.from_iterable(new_frontiers):
            visited_points.add(p)

        # bounds checking
        for index,frontier in enumerate(new_frontiers):
            if done_map[index]:
                continue
            if len(frontier) == 0:
                done_map[index] = True
                continue
            
            # check the points
            for x,y in frontier:
                if x < min_x or x > max_x or y < min_y or y > max_y:
                    # this has gone to infinity
                    done_map[index] = True
                    is_inf[index] = True
                    break
        
        # since any already visited points are removed,
        #   we only need to remove the ones where an overlap occurs 
        for index,frontier in enumerate(new_frontiers):
            # get this set minus all other sets:
            new_set = functools.reduce(
                lambda x,y: x-y, 
                itertools.chain(new_frontiers[:index], new_frontiers[index+1:]), 
                frontier,
            )
            results[index] += len(new_set)                 

    Part_1_Answer = max(
        map(
            lambda x: x[1],
            filter(
                lambda x: is_inf[x[0]] == False,
                enumerate(results),
            ),
        ),
    )


    ### Part 2
    
    # need to find one point that is inside the 10k set
    # guess is somewhere around the centroid of all points

    x_average = sum(map(lambda x: x[0], points)) // num_points
    y_average = sum(map(lambda x: x[1], points)) // num_points

    start_point = None

    for point in itertools.chain.from_iterable(generateManhattanNeighborsIncreasing((x_average, y_average))):
        if getAllDistScore(point, points) < ALL_DIST_LIMIT:
            print(f"Found a start candidate at {point}")
            start_point = point
            break

    assert(start_point is not None)

    visited = set()
    pending = deque()
    pending.append(start_point)

    Part_2_Answer = 0

    while pending:
        t = pending.popleft()

        if t in visited:
            continue
        
        visited.add(t)

        if getAllDistScore(t, points) < ALL_DIST_LIMIT:
            Part_2_Answer += 1
            pending.extend(generateManhattanNeighbors(t))
        else:
            continue

    return (Part_1_Answer, Part_2_Answer)