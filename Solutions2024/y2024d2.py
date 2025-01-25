from itertools import pairwise


def is_report_safe(report: list[int]) -> bool:
    """Check if a line is safe"""
    direction = 0
    for x,y in pairwise(report):
        if direction == 0:
            if x < y:
                direction = 1 
            elif x > y:
                direction = -1
            else:
                assert x == y
                return False
        elif direction == 1:
            if x >= y:
                return False
        elif direction == -1:
            if y >= x:
                return False

        if abs(x-y) > 3:
            return False
    return True



def y2024d2(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2024/d2.txt"
    print("2024 day 2:")

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

    # for multi line inputs

    Part_1_Answer = sum(1 for l in lineList if is_report_safe(list(map(int, l.split()))))

    Part_2_Answer = 0
    for l in lineList:
        l = list(map(int, l.split()))
        if is_report_safe(l):
            Part_2_Answer += 1
            continue
        
        # This could be better by noting where it failed in the `is_safe` check
        #   and only removing those certain indexes
        for i in range(len(l)):
            new_l = l[:i] + l[i+1:]
            if is_report_safe(new_l):
                Part_2_Answer += 1
                break

    return (Part_1_Answer, Part_2_Answer)