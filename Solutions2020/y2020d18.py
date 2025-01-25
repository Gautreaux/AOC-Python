# from AOC_Lib.name import *

from collections import deque


class Stack:
    def __init__(self, iterable) -> None:
        self.items = list(iterable)
        self.index = 0

    def peek(self):
        return self.items[self.index]

    # def push():
    #     pass

    def pop(self):
        k = self.peek()
        self.index += 1
        return k

    def __len__(self):
        return len(self.items) - self.index


operators = ["*", "+"]


def resolveToken(stack, exprResolver):
    e = stack.pop()
    if e in operators:
        return e
    try:
        return int(e)
    except ValueError:
        pass

    # need to resolve parens
    assert e == "("  # ) <- for formatter to behave
    pCount = 1
    partial = ""
    while pCount > 0:
        k = stack.pop()
        if k == ")":
            pCount -= 1
            if pCount > 0:
                partial += k + " "
        else:
            if k == "(":  # ) <- for formatter
                pCount += 1
            partial += k + " "
    return exprResolver(partial.strip())


def evaluateExpression(expr) -> int:
    stack = Stack(expr.split(" "))

    partialSum = resolveToken(stack, evaluateExpression)
    while len(stack) > 0:
        operator = resolveToken(stack, evaluateExpression)
        rhs = resolveToken(stack, evaluateExpression)

        assert operator in operators
        if operator == "+":
            partialSum += rhs
        elif operator == "*":
            partialSum *= rhs
    return partialSum


def initialFormatter(expr) -> str:
    return expr.replace("(", "( ").replace(")", " )")


# man i wish i had done a proper Dijkstras shunting yard
def part2EvaluteExpression(expr):
    stack = Stack(expr.split(" "))

    partialSum = resolveToken(stack, part2EvaluteExpression)
    while len(stack) > 0:
        operator = resolveToken(stack, part2EvaluteExpression)
        if operator == "+":
            partialSum += resolveAddRHS(stack)
        elif operator == "*":
            partialSum *= resolveMultRHS(stack)
    return partialSum


def resolveMultRHS(stack):
    e = resolveToken(stack, part2EvaluteExpression)
    while True:
        if len(stack) <= 0:
            return e
        op = stack.peek()
        if op == "*":
            return e
        assert op == "+"
        stack.pop()
        e += resolveToken(stack, part2EvaluteExpression)
    return e


def resolveAddRHS(stack):
    return resolveToken(stack, part2EvaluteExpression)


def y2020d18(inputPath=None):
    if inputPath == None:
        inputPath = "Input2020/d18.txt"
    print("2020 day 18:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    # for multi line inputs

    Part_1_Answer = sum(
        map(lambda x: evaluateExpression(initialFormatter(x)), lineList)
    )
    Part_2_Answer = sum(
        map(lambda x: part2EvaluteExpression(initialFormatter(x)), lineList)
    )

    return (Part_1_Answer, Part_2_Answer)
