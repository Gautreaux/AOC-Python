

from collections import deque
from typing import Any, Generator, Iterator, Iterable

import logging

def _PartitionIteratorHelper(iterator: Iterator[Any], seq: Iterable[Any],
    head_done_callback, tail_done_callback,
) -> Generator[Any, bool, None]:
    """All the logic for partition iterator"""

    # NOTE - len(seq) will be >= 1

    seq_as_tuple = tuple(seq)
    window = deque(maxlen=len(seq_as_tuple))
    pending_head = deque()
    to_yield = None
    
    try:
        # fill the window
        while len(window) < len(seq_as_tuple):
            n = next(iterator)
            window.append(n)
        
        if tuple(window) == seq_as_tuple:
            window = None
    except StopIteration:
        # the entire iterator was shorter than `seq`
        #   everything will be returned in `head`
        pending_head = window
        window = None

    logging.debug(f"Starting window is: {window}")

    while True:
        logging.debug(f"About to yield {to_yield}, window is {window}, pending head is {pending_head}")
        is_head = yield to_yield
        logging.debug(f'got is_head = {is_head}')

        # The end conditions need to be checked after each next() call
        while True:            
            # see if we can short circuit on head
            if is_head and len(pending_head) > 0:
                to_yield = pending_head.popleft()
                break

            if window is None:
                logging.debug("WIN_IS_NONE")
                if is_head:
                    # the head has already been exhausted
                    logging.debug("Window None HEAD stop iteration")
                    logging.debug("WNONE HEAD")
                    head_done_callback()
                    to_yield = None
                    break
                else:
                    logging.debug("WIN_IS_NONE_IS TAIL")
                    try:
                        to_yield = next(iterator)
                        break
                    except StopIteration as ex:
                        # TODO - cannot raise stop iteration in a generator? needs to return?
                        logging.debug("WNONE TAIL")
                        logging.debug("Window None TAIL stop iteration")
                        tail_done_callback()
                        to_yield = None
                        break
                # should be unreachable
                assert(False)

            # try to get a new value
            try:
                n = next(iterator)
            except StopIteration as ex:
                if is_head:
                    # the window never matched
                    #   so convert it to be head
                    assert(len(pending_head) == 0)
                    pending_head = window
                    window = None
                    continue
                else:
                    # There is nothing else to do here
                    logging.debug("Next Tail stop iteration")
                    tail_done_callback()
                    to_yield = None
                    break
                # should be unreachable
                assert(False)
            
            # there was a new valid value for n:
            #   update the window
            h = window.popleft()
            window.append(n)

            logging.debug(f"Pulled `{h}` from the iterator [{is_head}]")

            # check if the window now matches
            if (tuple(window) == seq_as_tuple):
                logging.debug(f"Window now matches")
                window = None

            # do something with the removed item
            logging.debug("A")
            if is_head:
                logging.debug("B1")
                to_yield = h
                break
            else:
                # add this as pending and try again
                logging.debug("B2")
                pending_head.append(h)
                continue
            # unreachable
            assert(False)


def PartitionIterator(iterator: Iterator[Any], seq: Iterable[Any]) -> tuple[Iterator[Any], Iterator[Any]]:
    """Partition the `iterator` on the first occurrence of `seq`
        returns a pair of iterators, one for the head and one for the tail
        will have minimal memory overhead if using the head tuple first

        Behavior roughly matchs that of str.partition(1)
    """

    try:
        seq_len = len(seq)
    except Exception:
        seq_len = None

    if seq_len == None:
        seq_len = sum(1 for _ in seq)
    
    if seq_len == 0:
        raise ValueError("empty separator")

    is_head_done = False
    is_tail_done = False

    def head_done_callback() -> None:
        nonlocal is_head_done
        is_head_done = True

    def tail_done_callback() -> None:
        nonlocal is_tail_done
        is_tail_done = True

    iterator_wrapper = _PartitionIteratorHelper(iterator, seq, head_done_callback, tail_done_callback)
    next(iterator_wrapper) # advance to the first yeld statement

    def _PartitionIterator(is_head: bool) -> Generator[Any, None, None]:
        nonlocal is_head_done
        nonlocal is_tail_done
        try:
            while True:
                k = iterator_wrapper.send(is_head)
                if (is_head and is_head_done) or ((not is_head) and is_tail_done):
                    return
                logging.debug(f"_PartIt<{is_head}> got {k}")
                yield k
        finally:
            logging.debug(f"_PartIt<{is_head}> stop iteration")
            

    return (iter(_PartitionIterator(True)), iter(_PartitionIterator(False)))


if __name__ == "__main__":
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Testing PartitionIterator")

    in_str = "pineapple"
    seqs = ["a", "p", "e", "ap", "pp", "pine", "apple", "pineapple", "z", "sierra", "pineapples"]
    for seq in seqs:
        logging.debug(f"Testing {in_str} on {seq}")
        lhs_expected,_,rhs_expected = in_str.partition(seq)
        lhs_itr, rhs_itr = PartitionIterator(iter(in_str), seq)
        logging.debug("BUILD LHS")
        lhs_str = "".join(list(lhs_itr))
        logging.debug("BUILD RHS")
        rhs_str = "".join(rhs_itr)
        logging.debug("BUILD DONE")

        logging.debug(f"For {in_str} {seq}")
        logging.debug(f"  LHS expected: {lhs_expected}, got {lhs_str}")
        logging.debug(f"  RHS expected: {rhs_expected}, got {rhs_str}")
        assert(lhs_expected == lhs_str)
        assert(rhs_expected == rhs_str)

    for seq in seqs:
        logging.debug(f"Testing {in_str} on {seq}")
        lhs_expected,_,rhs_expected = in_str.partition(seq)
        lhs_itr, rhs_itr = PartitionIterator(iter(in_str), seq)
        logging.debug("BUILD RHS")
        rhs_str = "".join(rhs_itr)
        logging.debug("BUILD LHS")
        lhs_str = "".join(list(lhs_itr))
        logging.debug("BUILD DONE")

        logging.debug(f"For {in_str} {seq}")
        logging.debug(f"  LHS expected: {lhs_expected}, got {lhs_str}")
        logging.debug(f"  RHS expected: {rhs_expected}, got {rhs_str}")
        assert(lhs_expected == lhs_str)
        assert(rhs_expected == rhs_str)

    in_str = ""
    lhs_itr, rhs_itr = PartitionIterator(iter(in_str), "seqs")
    assert("" == "".join(lhs_itr))
    assert("" == "".join(rhs_itr))
    
    logging.debug("Tests passing")
