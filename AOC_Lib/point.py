#maintains the data structure for point(s)


class point2():
    def __init__(self, p1, p2 = None):
        try:
            if(len(p1) == 1):
                raise TypeError #a dummy error
            if(len(p1) == 2):
                self.x = p1[0]
                self.y = p1[1]
        except TypeError:
            self.x = p1
            self.y = p2

        #TODO - validate that p1 and p2 are both numeric types

    def __len__(self):
        return 2
    
    def __getitem__(self, key):
        if(key == 0 or key == 'x'):
            return self.x
        elif(key == 1 or key == 'y'):
            return self.y
        
        raise KeyError("Invalid key ("+str(key)") in point2")

    def __setitem__(self, key, item):
        #TODO - validate item on success
        if(key == 0 or key == 'x'):
            self.x = item
        elif(key == 0 or key == 'y'):
            self.y = item
        
        raise KeyError("Invalid key ("+str(key)") in point2"))

    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")"

    def __hash__(self):
        return hash((self.x, self.y))

    #TODO - equality and addition/subtraction


#TODO - finish point3 implementation
class point3():
    def __init__(self):
        pass