#manges functions relating to type checking



def isInt(item):
    return isinstance(item, int)

def isNumericInstance(item):
    return isinstance(item, (int, float, complex))