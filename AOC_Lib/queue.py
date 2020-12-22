#implements the fifo queue adt

import itertools
from typing import Iterable


class Queue():
    def __init__(self):
        self.__q = []
        
    def __len__(self):
        return len(self.__q)

    def __contains__(self, item):
        return item in self.__q
    
    def pushBack(self, element):
        self.__q.append(element)
    
    def pop(self):
        t = self.__q[0]
        self.__q = self.__q[1:]
        return t

class EmptyQueueException(Exception):
    pass

class FullQueueException(Exception):
    pass

class CircularQueue():
    def __init__(self, maxSize, iterable : Iterable = None) -> None:
        self._q = [None]*maxSize
        self._next_pop = 0
        self._next_push = 0
        self._size = 0
        self._maxSize = maxSize

        if iterable is not None:
            for i in iterable:
                self.push(i)
    
    def __len__(self):
        return self._size

    def push(self, item):
        if len(self) == self._maxSize:
            raise FullQueueException
        self._q[self._next_push] = item
        self._next_push = (self._next_push + 1) % self._maxSize
        self._size += 1

    def peek(self):
        if len(self) == 0:
            raise EmptyQueueException()
        return self._q[self._next_pop]
    
    def pop(self):
        if len(self) == 0:
            raise EmptyQueueException()
        i = self._next_pop
        self._next_pop = (self._next_pop + 1 ) % self._maxSize
        self._size -= 1
        return self._q[i]

    def generatorNonConsuming(self):
        # probably shouldn't push/pop while this is running
        for i in range(len(self)):
            yield self._q[(self._next_pop + i) % self._maxSize]

    def generatorConsuming(self):
        # technically safe to push/pop while this is running
        try:
            while True:
                yield self.pop()
        except EmptyQueueException:
            pass

    def copyN(self, n=None):
        "copy the first n elements of the queue, up to current length"
        n_safe = min(n, len(self)) if n is not None else len(self)
        return CircularQueue(self._maxSize, itertools.islice(self.generatorNonConsuming(), n_safe))