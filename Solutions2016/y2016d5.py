# from AOC_Lib.name import *

from hashlib import md5


def inifiniteGenerator():
    i = 0
    while True:
        yield i
        i += 1


def hashGenerator(base):
    for i in inifiniteGenerator():
        s = md5(bytes(f"{base}{i}", "ascii")).hexdigest()
        if s.find("00000") != 0:
            continue
        print(s)
        yield (s)


def y2016d5(inputPath=None):
    if inputPath == None:
        inputPath = "Input2016/d5.txt"
    print("2016 day 5:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    doorCode = lineList[-1]

    matchingHashes = []

    myPassword = ""
    pt2Password = [None] * 8
    hashGen = hashGenerator(doorCode)
    while None in pt2Password:
        h = next(hashGen)

        if len(myPassword) < 8:
            myPassword += h[5]

        try:
            i = int(h[5])
            if pt2Password[i] is None:
                pt2Password[i] = h[6]
        except ValueError:
            pass
        except IndexError:
            pass

    Part_1_Answer = myPassword
    Part_2_Answer = "".join(pt2Password)

    # print(matchingHashes)

    return (Part_1_Answer, Part_2_Answer)
