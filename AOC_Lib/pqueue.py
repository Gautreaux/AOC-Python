import heapq


class PQElement:
    def __init__(self, value, priority):
        self.v = value
        self.p = priority

    def __lt__(self, other):
        return self.p < other.p


class PQueue:
    def __init__(self):
        self.__list = []

    def __len__(self):
        return len(self.__list)

    def push(self, item, priority):
        k = PQElement(item, priority)
        heapq.heappush(self.__list, k)

    def popMin(self):
        k = heapq.heappop(self.__list)
        return k.v
