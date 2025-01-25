# from AOC_Lib.name import *

from collections import defaultdict
import itertools

NUM_WORKERS = 5


def getTaskTime(task_name: str) -> int:
    assert len(task_name) == 1
    return 60 + ord(task_name) - (ord("A") - 1)


def y2018d7(inputPath=None):
    if inputPath == None:
        inputPath = "Input2018/d7.txt"
    print("2018 day 7:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    all_keys = set()
    # dependency store
    #   where the key is an item
    #   and the value(s list) is the items that require this to be completed
    #   before they can begin
    deps = defaultdict(list)

    for line in lineList:
        s = line.split(" ")
        pre = s[1]
        post = s[-3]
        assert len(pre) == 1
        assert len(post) == 1
        deps[pre].append(post)
        all_keys.add(pre)
        all_keys.add(post)

    # simple topological ordering

    indegree_dict = defaultdict(int)

    for v in deps.values():
        for l in v:
            indegree_dict[l] += 1

    avail = set()

    for k in all_keys:
        if indegree_dict[k] == 0:
            avail.add(k)

    out_order = []

    while avail:
        m = min(avail)
        avail.remove(m)
        out_order.append(m)

        for k in deps[m]:
            indegree_dict[k] -= 1
            if indegree_dict[k] < 0:
                raise RuntimeError("BAD")
            elif indegree_dict[k] == 0:
                avail.add(k)

    assert len(out_order) == len(all_keys)
    Part_1_Answer = "".join(out_order)

    # Part 2

    # reset things from above
    indegree_dict = defaultdict(int)

    for v in deps.values():
        for l in v:
            indegree_dict[l] += 1

    avail = set()

    for k in all_keys:
        if indegree_dict[k] == 0:
            avail.add(k)

    workers = []

    for this_time in itertools.count(0):
        new_workers = []

        # check which workers are/aren't done
        for w in workers:
            try:
                next(w[1])
                # this task is ongoing so re-append it
                new_workers.append(w)
            except StopIteration:
                # this task has been finished
                # update appropriately
                m = w[0]
                for k in deps[m]:
                    indegree_dict[k] -= 1
                    if indegree_dict[k] < 0:
                        raise RuntimeError("BAD")
                    elif indegree_dict[k] == 0:
                        avail.add(k)

        # assign tasks to free workers
        while avail and (len(new_workers) < NUM_WORKERS):
            m = min(avail)
            avail.remove(m)
            new_workers.append((m, iter(range(getTaskTime(m) - 1))))

        # print(f"{this_time} <{avail}>:{new_workers}")

        if new_workers:
            workers = new_workers
        else:
            Part_2_Answer = this_time
            break

    return (Part_1_Answer, Part_2_Answer)
