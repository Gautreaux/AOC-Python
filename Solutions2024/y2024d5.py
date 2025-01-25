# from AOC_Lib.name import *
from collections import defaultdict


def is_valid_print_order(print_order: list[int], keys_before_values: defaultdict[int, set]) -> bool:
    """Return true iff this is a valid print order"""

    for i in range(len(print_order)):
        active = print_order[i]
        for ii in range(i+1, len(print_order)):
            target = print_order[ii]

            if target not in keys_before_values[active]:
                return False

    return True

def get_valid_print_order(print_order: list[int], keys_before_values: defaultdict[int, set]) -> list[int]:
    """Return a valid print odering"""

    pending = set(print_order)
    ordering = []

    # This is just a topological sort,
    #   but somewhat lazily implemented
    indegrees = {p:0 for p in pending}
    for p in pending:
        for b in keys_before_values[p]:
            if b in pending:
                indegrees[b] += 1

    while indegrees:
        updated: bool = True
        for k,v in indegrees.items():
            if v == 0:
                ordering.append(k)
                indegrees.pop(k)
                updated = True

                for b in keys_before_values[k]:
                    if b in indegrees:
                        indegrees[b] -= 1
                
                break

        if not updated:
            raise RuntimeError('Cycle detected')

    return ordering


def y2024d5(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2024/d5.txt"
    print("2024 day 5:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    keys_before_values = defaultdict(set)
    manuals: list[list[int]] = []

    for line in lineList:
        if '|' in line:
            lhs, _, rhs = line.partition('|')
            keys_before_values[int(lhs)].add(int(rhs))
        elif ',' in line:
            manuals.append([int(l) for l in line.split(',')])
        elif not line:
            continue
        else:
            raise RuntimeError(f'Unrecognized line: {line}')
        
    Part_1_Answer = 0
    Part_2_Answer = 0

    def get_middle_page(m: list[list[int]]) -> int:
        assert m # is not empty
        assert len(m) % 2 == 1
        return m[len(m) // 2]

    for m in manuals:
        if is_valid_print_order(m, keys_before_values):
            Part_1_Answer += get_middle_page(m)
        else:
            m = get_valid_print_order(m, keys_before_values)
            Part_2_Answer += get_middle_page(m)

    return (Part_1_Answer, Part_2_Answer)