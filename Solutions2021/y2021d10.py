# from AOC_Lib.name import *

MATCH_TABLE = {
    ")" : "(",
    "]" : "[",
    "}" : "{",
    ">" : "<",
    "(" : ")",
    "[" : "]",
    "{" : "}",
    "<" : ">",
}

SCORE_TABLE = {
    ")" : 3,
    "]" : 57,
    "}" : 1197,
    ">" : 25137,
}

CLOSURE_SCORE_TABLE = {
    ")" : 1,
    "]" : 2,
    "}" : 3,
    ">" : 4,
}

#])}> for highlighter

OPENERS = "{(<["
CLOSURES = "]>)}"

def y2021d10(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2021/d10.txt"
    print("2021 day 10:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    score = 0
    closure_scores = []

    for line in lineList:
        s = []
        corrupt = False

        for c in line:
            if c in OPENERS:
                s.append(c)
            elif c in CLOSURES:
                cc = s.pop()

                if MATCH_TABLE[c] != cc:
                    score += SCORE_TABLE[c]
                    corrupt = True
                    break
            else:
                raise RuntimeError(f"Illegal char {c}")
            
        if corrupt:
            continue

        if len(s) == 0:
            # clean exit
            continue

        this_score = 0
        while s:
            c = s.pop()
            this_score = this_score * 5 + CLOSURE_SCORE_TABLE[MATCH_TABLE[c]]
        closure_scores.append(this_score)

    closure_scores.sort()

    Part_2_Answer = closure_scores[len(closure_scores) // 2]

    Part_1_Answer = score

    # assert(Part_2_Answer != 1237256840442)
    # assert(Part_2_Answer != 2937146265702)


    return (Part_1_Answer, Part_2_Answer)