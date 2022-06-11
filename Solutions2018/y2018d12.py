# from AOC_Lib.name import *
import collections
from itertools import islice
import itertools

# from the itertools docs
def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def advance(state: str, offset: int, plant_map: dict[str, str]) -> tuple[str, int]:
    """Advance one generation based on plant_map and return the new state and offset"""
    assert(set(state) == set("#."))
    o = []
    # only need to pad so that 4 empties on either side
    for i in sliding_window(itertools.chain("....", state, "...."), 5):
        i = "".join(i)
        if i not in plant_map:
            print(i)
        assert(i in plant_map)
        o.append(plant_map[i])

    # pop empties off of o
    while o:
        if o[-1] == ".":
            o.pop()
        else:
            break

    # pop off the front
    # s = sum(1 for _ in itertools.takewhile(lambda x: x == '.', o))
    k = "".join(itertools.dropwhile(lambda x: x == '.', o))
    num_dropped = len(o) - len(k)
    return (k, offset-2+num_dropped)


def y2018d12(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2018/d12.txt"
    print("2018 day 12:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    # for multi line inputs

    plant_map = {}

    itr = iter(lineList)

    start = next(itr)

    for line in itr:
        if not line:
            continue
        a,_,b = line.partition(" => ")
        assert(b in ["#", "."])
        assert(len(a) == 5)
        plant_map[a] = b

    ist = start.partition("initial state: ")[-1]
    offset = 0

    for _ in range(20):
        ist, offset = advance(ist, offset, plant_map)
    
    e = zip(itertools.count(offset), ist)
    f = filter(lambda x: x[1] == '#', e)
    Part_1_Answer = sum(map(lambda x: x[0], f))

    # part 2
    ist = start.partition("initial state: ")[-1]
    offset = 0

    h_cache = {}

    h_cache[ist] = {0,0}
    
    first_loop_index = None
    loop_state = None
    first_loop_offset = None

    for i in range(5000):
        if i % 1000 == 0:
            print(f"i = {i}")
        ist, offset = advance(ist, offset, plant_map)
        if ist in h_cache:
            print(f"Loop occurs at i = {i}, {offset} from {h_cache[ist]}")
            print("\t", ist)
            first_loop_index = i
            loop_state = ist
            first_loop_offset = offset
            base_loop_index, base_loop_offset = h_cache[ist]
            break
        else:
            h_cache[ist] = (i,offset)  

    assert(first_loop_index is not None)

    target = 50000000000

    loop_size = first_loop_index - base_loop_index
    offset_per_loop = first_loop_offset - base_loop_offset

    assert(loop_size == 1)
    target = target - base_loop_index
    
    new_offset = target * offset_per_loop

    e = zip(itertools.count(new_offset), loop_state)
    f = filter(lambda x: x[1] == '#', e)
    Part_2_Answer = sum(map(lambda x: x[0], f))

    # TODO - just some off by one errors to solve for
    assert(Part_2_Answer > 2649999996756)

    return (Part_1_Answer, Part_2_Answer)