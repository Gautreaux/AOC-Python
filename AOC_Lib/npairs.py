def allPairsGenerator(listIn, independentPairs=True):
    """generate all pairs from the list"""
    l = len(listIn)
    for i in range(l):
        for j in range(i + (1 if independentPairs else 0), l):
            yield (listIn[i], listIn[j])


def allTriplesGenerator(listIn, independentPairs=True):
    """generate all triples from the list"""
    l = len(listIn)
    for i in range(l):
        for j in range(i + (1 if independentPairs else 0), l):
            for k in range(j + (1 if independentPairs else 0), l):
                yield (listIn[i], listIn[j], listIn[k])


def allQuadsGenerator(listIn, independentPairs=True):
    """generate all Quads from the list"""
    l = len(listIn)
    for i in range(l):
        for j in range(i + (1 if independentPairs else 0), l):
            for k in range(j + (1 if independentPairs else 0), l):
                for m in range(k + (1 if independentPairs else 0), l):
                    yield (listIn[i], listIn[j], listIn[k], listIn[m])
