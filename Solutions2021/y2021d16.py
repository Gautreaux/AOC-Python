# from AOC_Lib.name import *

from collections import namedtuple
import functools
import itertools
from typing import Generator, Iterable

from operator import mul, add

Packet_T = namedtuple("Packet_T", "version_id type_id literal length_type_id sub_packets")

type_reductions = {
    0 : add,
    1 : mul,
    2 : min,
    3 : max,
    5 : lambda x,y: 1 if x > y else 0,
    6 : lambda x,y: 1 if x < y else 0,
    7 : lambda x,y: 1 if x == y else 0
}

def asBitData(s: str) -> Iterable[int]:
    for c in s:
        bits = "{:04b}".format(int(c, base=16))
        for b in bits:
            yield int(b)


def parseNBitValue(i: Iterable[int], n:int) -> int:
    """Parse an n-bit value"""
    c = 0
    for _ in range(n):
        a = next(i)
        c = (c<<1) + a
    return c


def parseLiteral(i: Iterable[int]) -> int:
    """Parse a literal out of the stream"""
    c = 0
    while True:
        a = next(i)
        v = parseNBitValue(i,4)
        c = (c<<4) + v

        if a == 0:
            break
    return c


def parsePacket(i: Iterable[int]) -> Packet_T:
    """Parse a single packet out of the stream"""
    version_id = parseNBitValue(i, 3)
    type_id = parseNBitValue(i, 3)

    literal = None
    length_type_id = None
    sub_packets = []

    if type_id == 4:
        literal = parseLiteral(i)
    else:
        # this is an operator
        length_type_id = next(i)
        if length_type_id == 0:
            total_bits_in_sub = parseNBitValue(i, 15)
            sub_i = itertools.islice(i, total_bits_in_sub)
            sub_packets.extend(parseAllPackets(sub_i))
        else:
            number_sub = parseNBitValue(i, 11)

            for _ in range(number_sub):
                sub_packets.append(parsePacket(i))
    
    return Packet_T(
        version_id=version_id,
        type_id=type_id,
        literal=literal,
        length_type_id=length_type_id,
        sub_packets=sub_packets,
    )


def parseAllPackets(i : Iterable[int]) -> Generator[Packet_T, None, None]:
    """Parse Packets from the iterable until exhausted"""
    while True:
        try:
            t = next(i)
        except StopIteration:
            break
        n_i = itertools.chain([t], i)
        p = parsePacket(n_i)
        yield p


def PreorderTraversal(p: Packet_T) -> Generator[Packet_T, None, None]:
    """Do a preorder traversal on the packets"""
    yield p
    for k in p.sub_packets:
        for sp in PreorderTraversal(k):
            yield sp


def evaluatePacket(p: Packet_T) -> int:
    """Return the value of iterating the packet tree"""
    
    if p.type_id == 4:
        return p.literal
    
    sub_values = map(evaluatePacket, p.sub_packets)
    return functools.reduce(type_reductions[p.type_id], sub_values)
    

def y2021d16(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2021/d16.txt"
    print("2021 day 16:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    assert(len(lineList) == 1)

    # Some tests:
    assert(parseLiteral(map(int, "101111111000101")) == 2021)

    _more_tests = {
        "C200B40A82": 3,
        "04005AC33890": 54,
        "880086C3E88112": 7,
        "CE00C43D881120": 9,
        "D8005AC2A8F0": 1,
        "F600BC2D8F": 0,
        "9C005AC2F8F0": 0,
        "9C0141080250320F1802104A08": 1,
    }

    for k,v in _more_tests.items():
        p = parsePacket(asBitData(k))
        e = evaluatePacket(p)
        if e != v:
            print(f"In packet `{k}` expected `{v}` but got `{e}`")
        assert(e == v)

    # And now our regularly scheduled programming

    packet = parsePacket(asBitData(lineList[0]))

    Part_1_Answer = sum(map(lambda x: x.version_id, PreorderTraversal(packet)))
    Part_2_Answer = evaluatePacket(packet)

    return (Part_1_Answer, Part_2_Answer)