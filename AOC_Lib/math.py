
from math import gcd

def elementwiseMultiplication(iterable) -> float:
    v = 1
    for e in iterable:
        v *= e
    return v

# can be replaced by math.lcm in python 3.9
def lcm(a:int, b:int) -> int:
    '''Return the least common multiple of a and b'''
    return abs(a*b) // gcd(a, b)