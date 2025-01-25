# from AOC_Lib.name import *


def y2021d3(inputPath=None):
    if inputPath == None:
        inputPath = "Input2021/d3.txt"
    print("2021 day 3:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    pos_counter = []
    while len(pos_counter) < len(lineList[0]):
        pos_counter.append([0, 0])

    for line in lineList:
        for i, c in enumerate(line):
            pos_counter[i][0 if c == "0" else 1] += 1

    print(pos_counter)

    gamma_rate_s = "".join(map(lambda x: "0" if x[0] > x[1] else "1", pos_counter))
    epsilon_rate_s = "".join(map(lambda x: "0" if x[0] < x[1] else "1", pos_counter))

    gamma_rate = int(gamma_rate_s, base=2)
    epsilon_rate = int(epsilon_rate_s, base=2)

    Part_1_Answer = gamma_rate * epsilon_rate

    # for part 2
    def filter_list(mo_list, lcb: bool):
        offset = 0
        while True:
            ctr = [0, 0]
            for line in mo_list:
                ctr[0 if line[offset] == "0" else 1] += 1

            if lcb:
                match_num = "1" if ctr[0] > ctr[1] else "0"
            else:
                match_num = "0" if ctr[0] > ctr[1] else "1"

            mo_list = list(filter(lambda x: x[offset] == match_num, mo_list))

            if len(mo_list) == 0:
                raise RuntimeError("NOTHING LEFT BAD")
            elif len(mo_list) == 1:
                return mo_list[0]
            else:
                offset += 1

    o2_s = filter_list(lineList, lcb=False)
    co2_s = filter_list(lineList, lcb=True)

    o2_rating = int(o2_s, base=2)
    co2_rating = int(co2_s, base=2)

    Part_2_Answer = o2_rating * co2_rating

    return (Part_1_Answer, Part_2_Answer)
