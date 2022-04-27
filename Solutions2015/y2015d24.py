# from AOC_Lib.name import *

import itertools
import functools
from operator import ge, mul

def anyNPackagesWeighK(num_packages:int, goal_weight:int, packages: set[int]) -> bool:
    """Return True iff any N (unique) packages combine to weigh goal_weight"""

    assert(goal_weight > 0)
    assert(num_packages > 0)
    if num_packages == 1:
        return goal_weight in packages

    # need to freeze the packages so that 
    for p in list(packages):
        remain_weight = goal_weight - p
        if remain_weight > 0:
            packages.remove(p)
            try:
                b = anyNPackagesWeighK(num_packages-1, remain_weight, packages)
            finally: 
                packages.add(p)
            if b:
                return True
    return False


def getLowestQEforNandK(num_packages:int, goal_weight: int, packages: set[int]) -> int:
    """Return the lowest QE value for the first ideal value"""
    # there is a more efficient way to calculate this: you want to prioritize picking from the ouside
    #   i.e. 1, 113 is 114 weight but only 113 QE 
    #       whereas 5, 109 is 114 weight but 545 QE
    # for now though, this should run fast enough
    return min(
        map((lambda x: functools.reduce(mul, x)), 
            filter((lambda x: sum(x) == goal_weight),
                itertools.combinations(packages, num_packages)
            )
        ) 
    )


def getSomePlacement(package_weights: set[int], num_groups: int) -> int:
    total_weight = sum(package_weights)
    assert(total_weight % num_groups == 0)
    target_weight = total_weight // num_groups
    print("Target weight is: ", target_weight)
    
    smallest_set_cardinality = -1
    for i in range(1, len(package_weights)):
        if anyNPackagesWeighK(i, target_weight, package_weights):
            # TODO - need to check that can construct two other groups
            #   that equal the right weight
            # **apparently not** (probably should still check tho)
            smallest_set_cardinality = i
            break

    print("The smallest set has {} packages in it".format(smallest_set_cardinality))
    return getLowestQEforNandK(i, target_weight, package_weights)


def y2015d24(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d24.txt"
    print("2015 day 24:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    package_weights = set(map(int, lineList))
    
    assert(len(package_weights) == len(lineList))

    Part_1_Answer = getSomePlacement(package_weights, 3)
    Part_2_Answer = getSomePlacement(package_weights, 4)


    return (Part_1_Answer, Part_2_Answer)