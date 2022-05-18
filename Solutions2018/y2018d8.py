# from AOC_Lib.name import *

from collections import namedtuple
from enum import Enum, unique
import functools


NodeData_T = namedtuple("NodeData_T", "start_index num_children num_meta")

NodeIndex_T = namedtuple("NodeIndex_T", "start_index child_list meta_list")


@unique
class OperatorEnum(Enum):
    """Types of operators"""
    HEADER = 0
    METADATA = 1
    END_NODE = 255


value_cache = {}

def _getNodeValue(data:NodeIndex_T, nodes: dict[int, NodeIndex_T]) -> int:
    if len(data.child_list) == 0:
        # simply sum the meta data
        return sum(data.meta_list)
    
    s = 0

    for child_index in data.meta_list:
        if child_index == 0:
            continue

        try:
            child_node = nodes[data.child_list[child_index - 1]]
        except IndexError:
            continue
        # KeyError would indicate a problem

        s += getNodeValue(child_node, nodes)
    return s


def getNodeValue(data:NodeIndex_T, nodes: dict[int, NodeIndex_T]) -> int:
    """Get the score value for the node"""
    global value_cache

    if data.start_index in value_cache:
        return value_cache[data.start_index]
    else:
        k = _getNodeValue(data, nodes)
        value_cache[data.start_index] = k
        return k


def y2018d8(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2018/d8.txt"
    print("2018 day 8:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    assert(len(lineList) == 1)

    tokens = list(map(int,lineList[0].split(" ")))
    metadata_sum = 0
    operator_stack = [OperatorEnum.HEADER]
    nodes_start_stack = []
    finished_metadata_stack = []
    finished_nodes_stack = []

    nodes: dict[int, NodeIndex_T] = {}

    tkn_iter = enumerate(tokens)
    for i,t in tkn_iter:
        if len(operator_stack) == 0:
            raise RuntimeError("Should not be able to empty the operator stack")

        op = operator_stack.pop()

        if op == op.END_NODE:
            # do some processing
            details: NodeData_T = nodes_start_stack.pop()
            meta = []
            children = []
            for _ in range(details.num_meta):
                assert(len(finished_metadata_stack) > 0)
                meta.append(finished_metadata_stack.pop())
            for _ in range(details.num_children):
                assert(len(finished_nodes_stack) > 0)
                children.append(finished_nodes_stack.pop())
            # meta.reverse() # ordering here does not matter
            children.reverse()
            nodes[details.start_index] = NodeIndex_T(details.start_index, children, meta)
            finished_nodes_stack.append(details.start_index)

            # and fix
            op = operator_stack.pop()
            assert(op != op.END_NODE)

        if op == op.METADATA:
            metadata_sum += t
            finished_metadata_stack.append(t)
        elif op == op.HEADER:
            num_children = t
            num_meta = next(tkn_iter)[1]
            operator_stack.append(OperatorEnum.END_NODE)
            for _ in range(num_meta):
                operator_stack.append(OperatorEnum.METADATA)
            for _ in range(num_children):
                operator_stack.append(OperatorEnum.HEADER)
            nodes_start_stack.append(NodeData_T(i, num_children, num_meta))
        else:
            raise NotImplementedError(op)

    print(operator_stack)
    print(finished_nodes_stack)
    print(finished_metadata_stack)
    print(nodes_start_stack)
    print("----------")

    while operator_stack and (operator_stack[-1] == OperatorEnum.END_NODE):
        operator_stack.pop()
        details: NodeData_T = nodes_start_stack.pop()
        meta = []
        children = []
        for _ in range(details.num_meta):
            assert(len(finished_metadata_stack) > 0)
            meta.append(finished_metadata_stack.pop())
        for _ in range(details.num_children):
            assert(len(finished_nodes_stack) > 0)
            children.append(finished_nodes_stack.pop())
        # meta.reverse() # ordering here does not matter
        children.reverse()
        nodes[details.start_index] = NodeIndex_T(details.start_index, children, meta)

    if len(operator_stack) != 0:
        raise RuntimeError("There should not be operators left on the operator stack")

    assert(len(operator_stack) == 0)
    assert(len(finished_metadata_stack) == 0)
    assert(len(finished_nodes_stack) == 0)
    assert(len(nodes_start_stack) == 0)


    Part_1_Answer = metadata_sum

    # Part 2

    meta_alt = sum(map(lambda x: sum(x.meta_list), nodes.values()))
    assert(meta_alt == metadata_sum)

    k = list(nodes.keys())
    k.sort()
    for _,k in zip(range(10), k):
        print(nodes[k])
    
    for i in [10, 8, 29, 45, 6]:
        print(f"Node {i} value: {getNodeValue(nodes[i], nodes)}")

    Part_2_Answer = getNodeValue(nodes[0], nodes)

    return (Part_1_Answer, Part_2_Answer)