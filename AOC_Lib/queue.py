#implements the fifo queue adt

class Queue():
    def __init__(self):
        self.__q = []
        
    def __len__(self):
        return len(self.__q)
    
    def pushBack(self, element):
        self.__q.append(element)
    
    def pop(self):
        t = self.__q[0]
        self.__q = self.__q[1:]
        return t