# from AOC_Lib.name import *

import itertools

def getMaxHappiness(person_pair_list):
    max_happiness = 0
    for p in itertools.permutations(person_pair_list.keys(), len(person_pair_list)):
        i = iter(p)
        i = itertools.chain(i, [next(i)])

        happiness = sum(
            map(
                (lambda x,y: person_pair_list[x][y] + person_pair_list[y][x]),
                p,
                i,
            )
        )

        max_happiness = max(max_happiness, happiness)
    return max_happiness

def y2015d13(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d13.txt"
    print("2015 day 13:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    person_pair_list = {}
    for line in lineList:
        s = line.split(" ")

        # t = (s[0], s[2], int(s[3]), s[-1][:-1])
        if s[0] not in person_pair_list:
            person_pair_list[s[0]] = {}
        
        person_pair_list[s[0]][s[-1][:-1]] = int(s[3]) * (1 if s[2] == "gain" else -1)

    Part_1_Answer = getMaxHappiness(person_pair_list)

    for v in person_pair_list.values():
        v["self"] = 0
    
    person_pair_list["self"] = {}
    for k in person_pair_list:
        person_pair_list["self"][k] = 0

    Part_2_Answer = getMaxHappiness(person_pair_list)

    return (Part_1_Answer, Part_2_Answer)