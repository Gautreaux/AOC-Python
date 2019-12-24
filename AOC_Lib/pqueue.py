import heapq

class PQElement():
    num = 0

    def __init__(self, value, priority):
        self.v = value
        self.p = priority
        self.n = PQElement.num
        PQElement.num+=1
    
    def __lt__(self, other):
        if(self.p == other.p):
            return self.n < other.n
        return self.p < other.p

    def __eq__(self, other):
        return self.p == other.p

class PQueue():
    def __init__(self):
        self.__list = []
    
    def __len__(self):
        return len(self.__list)
    
    def push(self, item, priority):
        k = PQElement(item, priority)
        heapq.heappush(self.__list, k)
    
    def popMin(self):
        #TODO - this needs to pop items so that priority ties are solved by insertion order
        k = heapq.heappop(self.__list)
        return k.v
