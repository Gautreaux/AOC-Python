# from AOC_Lib.name import *


def checkValid(passport:str) -> bool:

    expected = {
        'byr':1,
        'iyr':1,
        'eyr':1,
        'hgt':1,
        'hcl':1,
        'ecl':1,
        'pid':1,
        'cid':0,
    }

    while passport.find("  ") != -1:
        passport.replace("  ", " ")
    fields = passport.strip().split(" ")
    for f in fields:
        e = f.split(":")

        if(len(e) != 2):
            print(e)
            print(f)
            print(fields)
            print(passport)
        assert(len(e) == 2)

        k = e[0]
        v = e[1]

        if k == 'cid':
            continue
        else:
            if k in expected:
                expected[k] -= 1
            else:
                return False
    
    return sum(map(lambda x: x[1], expected.items())) == 0

def byrValid(v):
    if len(v) != 4:
        return False
    for c in v:
        if c not in ['0','1','2','3','4','5','6','7','8','9']:
            return False
    try:
        k = int(v)
    except ValueError:
        return False
    
    return k >= 1920 and k <= 2002

def iyrValid(v):
    if len(v) != 4:
        return False
    for c in v:
        if c not in ['0','1','2','3','4','5','6','7','8','9']:
            return False
    try:
        k = int(v)
    except ValueError:
        return False
    
    return k >= 2010 and k <= 2020

def eyrValid(v):
    if len(v) != 4:
        return False
    for c in v:
        if c not in ['0','1','2','3','4','5','6','7','8','9']:
            return False
    try:
        k = int(v)
    except ValueError:
        return False
    
    return k >= 2020 and k <= 2030

def hgtValid(v):
    try:
        i = int(v[:-2])
    except ValueError:
        return False
    u = v[-2:]

    if u == "cm":
        return i >= 150 and i <= 193
    elif u == 'in':
        return i >= 59 and i <= 76
    else:
        return False

def hclValid(v):
    if len(v) != 7:
        return False
    
    if v[0] != '#':
        return False

    for c in v[1:]:
        if c not in ['0','1','2','3','4','5','6','7','8','9', 'a', 'b', 'c', 'd', 'e','f']:
            return False
    return True

def eclValid(v):
    if len(v) != 3:
        return False
    
    return v in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

def pidValid(v):
    if len(v) != 9:
        return False
    for c in v:
        if c not in ['0','1','2','3','4','5','6','7','8','9']:
            return False
    return True

def checkValid2(passport:str) -> bool:

    expected = {
        'byr':1,
        'iyr':1,
        'eyr':1,
        'hgt':1,
        'hcl':1,
        'ecl':1,
        'pid':1,
        'cid':0,
    }

    checkers = {
        'byr':byrValid,
        'iyr':iyrValid,
        'eyr':eyrValid,
        'hgt':hgtValid,
        'hcl':hclValid,
        'ecl':eclValid,
        'pid':pidValid,
    }

    while passport.find("  ") != -1:
        passport.replace("  ", " ")
    fields = passport.strip().split(" ")
    for f in fields:
        e = f.split(":")

        if(len(e) != 2):
            print(e)
            print(f)
            print(fields)
            print(passport)
        assert(len(e) == 2)

        k = e[0]
        v = e[1]

        if k == 'cid':
            continue
        else:
            if k in expected:
                if checkers[k](v) is False:
                    return False
                expected[k] -= 1
            else:
                return False
    
    return sum(map(lambda x: x[1], expected.items())) == 0


# sample variant for reading data from an input file, line by line
def y2020d4(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2020/d4.txt"
    print("2020 day 4:")

    Part_1_Answer = 0
    Part_2_Answer = 0
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    lineList.append("")

    # for multi line inputs 
    thisPassport = ""
    for line in lineList:
        if line == "":
            if checkValid(thisPassport) is True:
                Part_1_Answer += 1
            if checkValid2(thisPassport) is True:
                Part_2_Answer += 1
            thisPassport = ""
        else:
            thisPassport += line + " "

    return (Part_1_Answer, Part_2_Answer)