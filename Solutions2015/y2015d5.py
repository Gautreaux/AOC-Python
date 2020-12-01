# from AOC_Lib.name import *

def isNice(s:str) -> bool:
    vowels = ['a','e', 'i','o','u']
    illegals = ['ab', 'cd', 'pq', 'xy']

    for i in illegals:
        if i in s:
            return False

    vowelCount = 0
    doubleCount = 0

    if s[-1] in vowels:
        vowelCount+=1

    for i in range(len(s) - 1):
        if s[i] == s[i+1]:
            doubleCount += 1
        if s[i] in vowels:
            vowelCount += 1
        
    return (vowelCount >= 3 and doubleCount >= 1)


def isNice2(s:str) -> bool:
    splitCount = 0

    for i in range(len(s) - 2):
        if s[i] == s[i+2]:
            splitCount += 1
            break
    
    if splitCount < 1:
        return False

    for i in range(len(s) - 3):
        if s[i:i+2] in s[i+2:]:
            return True
        
    return False

# sample variant for reading data from an input file, line by line
def y2015d5(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d5.txt"
    print("2015 day 5:")

    Part_1_Answer = None
    Part_2_Answer = None

    niceCount = 0
    niceCount2 = 0

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            if isNice(line):
                niceCount += 1

            if isNice2(line):
                niceCount2 += 1

    Part_1_Answer = niceCount
    Part_2_Answer = niceCount2
        
    return (Part_1_Answer, Part_2_Answer)
