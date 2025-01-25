# from AOC_Lib.name import *
from typing import Iterator
import itertools

def p1_tokens(line: str) -> Iterator[int]:
    for c in line:
        if c in '0123456789':
            yield int(c)

def p2_tokens(line: str) -> Iterator[int]:
    raise RuntimeError('Not Working Right')
    digits = {
    '0': 0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'0':0,'one':1, 'two':2, 'three':3, 'four':4, 'five':5,'six':6,'seven':7,'eight':8, 'nine':9
    }

    candidates = {}

    for c in line:
        print(candidates)
        d = digits.get(c)
        if d is not None:
            yield d
            candidates = {}
            continue

        d = candidates.get(c)
        if d is not None:
            yield d
            continue

        candidates = dict(itertools.chain(((k[1:],v) for k,v in candidates.items() if k.startswith(c)), ((k[1:],v) for k,v in digits.items() if k.startswith(c))))

def p2_tokens_brute(line: str) -> Iterator[int]:

    words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

    for i in range(len(line)):
        if line[i] in '0123456789':
            yield int(line[i])

        for d, n in enumerate(words):
            if line.startswith(n, i):
                yield d+1
        

def y2023d1(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2023/d1.txt"
    print("2023 day 1:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    Part_1_Answer = 0
    Part_2_Answer = 0

    for line in lineList:
        # digits = list(p1_tokens(line))
        # print('p1:', digits)
        # Part_1_Answer += (digits[0]*10 + digits[-1])
        digits = list(p2_tokens_brute(line))
        print('p2:', digits)
        Part_2_Answer += (digits[0]*10 + digits[-1])

    print(Part_2_Answer)
    assert Part_2_Answer > 53293
    assert Part_2_Answer > 53303

    return (Part_1_Answer, Part_2_Answer)
