# from AOC_Lib.name import *

from typing import List, Optional, Union


def matchRuleAllGenerator(message, startingInd, ruleNum, ruleSet):
    "Generates all possible next starting positions that are reachable from this rule"
    for r in ruleSet[ruleNum]:
        for s in applyRuleCaseGenerator(message, startingInd, r, ruleSet):
            yield s


# rewriting as generators for part two


def applyRuleCaseGenerator(message: str, startingInd: int, rule, ruleSet):
    "Generates all possible next starting positions that are reachable from this particular case"
    if type(rule[0]) == int:
        # input is a list of possible sub rules
        # TODO - how to update for the subsequent rules
        # need to propagate s for all possible
        if len(rule) == 1:
            for s in matchRuleAllGenerator(message, startingInd, rule[0], ruleSet):
                yield s
        elif len(rule) == 2:
            for s in matchRuleAllGenerator(message, startingInd, rule[0], ruleSet):
                for ss in matchRuleAllGenerator(message, s, rule[1], ruleSet):
                    yield ss
        elif len(rule) == 3:
            for s in matchRuleAllGenerator(message, startingInd, rule[0], ruleSet):
                for ss in matchRuleAllGenerator(message, s, rule[1], ruleSet):
                    for sss in matchRuleAllGenerator(message, ss, rule[2], ruleSet):
                        yield sss
        else:
            raise NotImplementedError()
    else:
        # single char
        assert len(rule) == 1
        assert type(rule[0]) == str
        if startingInd >= len(message):
            return
        if message[startingInd] == rule[0]:
            yield startingInd + 1
        else:
            return


def y2020d19(inputPath=None):
    if inputPath == None:
        inputPath = "Input2020/d19.txt"
    print("2020 day 19:")

    # print("DEBUGGING ON")
    # inputPath = "Input2020/d19-sample.txt"

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    rules = []
    messages = []

    def lineGen():
        for l in lineList:
            yield l

    ll = lineGen()

    for l in ll:
        if l == "":
            break
        rules.append(l)
    for l in ll:
        messages.append(l)

    # parse rules
    ruleDict = {}
    for r in rules:
        s = r.split(" ", 1)
        assert s[0][-1] == ":"
        num = int(s[0][:-1])

        # parse multiple rules
        ss = s[1].replace('"', "").split(" ")
        thisRules = []
        partialRule = []
        for e in ss:
            if e == "|":
                assert partialRule != []
                thisRules.append(partialRule)
                partialRule = []
            else:
                try:
                    i = int(e)
                    # now we know its an integer
                    partialRule.append(i)
                except ValueError:
                    # character literal
                    assert partialRule == []
                    thisRules.append([e])
        if partialRule != []:
            thisRules.append(partialRule)
        ruleDict[num] = thisRules

    # # legacy part1 implementation
    # total = 0
    # for msg in messages:
    #     k = matchRuleAll(msg, 0, 0, ruleDict)
    #     if k is not None and k == len(msg):
    #         total += 1
    # Part_1_Answer = total

    # generator based part 1 implementation
    total = 0
    for msg in messages:
        for k in matchRuleAllGenerator(msg, 0, 0, ruleDict):
            if k == len(msg):
                total += 1
                break
    # print(f"Generator part 1 answer: {total}")
    # Part_1_Answer = f"{Part_1_Answer} == {total}?"
    Part_1_Answer = total

    # updating the grammer for part 2
    ruleDict[8] = [[42], [42, 8]]
    ruleDict[11] = [[42, 31], [42, 11, 31]]

    total = 0
    for msg in messages:
        for k in matchRuleAllGenerator(msg, 0, 0, ruleDict):
            if k == len(msg):
                total += 1
                break
    Part_2_Answer = total

    return (Part_1_Answer, Part_2_Answer)


######################
# Legacy Part 1 Implementation Follows

# def matchRuleCase(message : str, startingInd : int, rule : List[Union[str,int]], ruleset) -> Optional[int]:
#     "Match a rule against a the message, returning the next starting index if successful"
#     if type(rule[0]) == int:
#         # input is a list of possible sub rules
#         for r in rule:
#             s = matchRuleAll(message, startingInd, r, ruleset)
#             if s == None:
#                 return None
#             else:
#                 startingInd = s
#         return startingInd
#     else:
#         # single char
#         assert(len(rule) == 1)
#         assert(type(rule[0]) == str)
#         if message[startingInd] == rule[0]:
#             return startingInd + 1
#         else:
#             return None

# def matchRuleAll(message : str, startingInd : int, ruleNum : int, ruleSet):
#     "Attempt to match rule components against the message, returning the next starting index if successful"
#     for r in ruleSet[ruleNum]:
#         s = matchRuleCase(message, startingInd, r, ruleSet)
#         if s == None:
#             continue
#         else:
#             startingInd = s
#             return startingInd
#     return None
