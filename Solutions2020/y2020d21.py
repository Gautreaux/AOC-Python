# from AOC_Lib.name import *

from copy import deepcopy
from typing import Counter

def y2020d21(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2020/d21.txt"
    print("2020 day 21:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    # print("DEBUG MODE ON")
    # lineList = ["mxmxvkd kfcds sqjhc nhms (contains dairy, fish)",
    #             "trh fvjkl sbzzf mxmxvkd (contains dairy)",
    #             "sqjhc fvjkl (contains soy)",
    #             "sqjhc mxmxvkd sbzzf (contains fish)"]
    
    recipesList = []

    for l in lineList:
        assert(l[-1] == ')')
        s = l.replace(")", "").replace(", ", " ").split(" ")
        i = iter(s)

        ingredients = []
        allergens = []

        while True:
            t = next(i)

            if t.find("(") != -1: # ) # for auto formatter
                break
            else:
                ingredients.append(t)
        
        while True:
            try:
                t = next(i)
                allergens.append(t)
            except StopIteration:
                break
        
        recipesList.append((ingredients, allergens))

    def allergensGenerator():
        for r in recipesList:
            for a in r[1]:
                yield a
    
    def ingredientsGenerator():
        for r in recipesList:
            for i in r[0]:
                yield i
    
    allAllergens = set(allergensGenerator())
    allIngredients = set(ingredientsGenerator())

    # print(allAllergens)
    # print(allIngredients)

    ingredientsDict = {}
    for i in allIngredients:
        ingredientsDict[i] = set()

    # add all the possible allergens to each ingredient
    for recipe in recipesList:
        for allergen in recipe[1]:
            for ingredient in recipe[0]:
                ingredientsDict[ingredient].add(allergen)

    # # remove the not possible allergens
    # for recipe in recipesList:
    #     for allergen in allAllergens:
    #         if allergen in recipe[1]:
    #             pass
    #         else:
    #             for i in recipe[0]:
    #                 s = ingredientsDict[i]
    #                 if allergen in s:
    #                     ingredientsDict[i].remove(allergen)

    allergensDict = {}
    for a in allAllergens:
        allergensDict[a] = []

    for recipe in recipesList:
        for allergen in recipe[1]:
            allergensDict[allergen].append(set(recipe[0]))


    allergensToMatch = deepcopy(allAllergens)
    allergensMatched = {}
    lastToMatch = len(allergensToMatch)+1

    while True:
        if len(allergensToMatch) == 0:
            break
        elif len(allergensToMatch) == lastToMatch:
            raise RuntimeError("LOOP")
        lastToMatch = len(allergensToMatch)

        for allergen, knownRecpies in allergensDict.items():
            if allergen in allergensMatched:
                continue

            if len(knownRecpies) > 1:
                i = knownRecpies[0].intersection(*(knownRecpies[1:]))
            else:
                assert(len(knownRecpies) == 1)
                i = knownRecpies[0]
            for am in allergensMatched.values():
                if am in i:
                    i.remove(am)

            if len(i) == 1:
                allergensMatched[allergen] = next(iter(i))
                allergensToMatch.remove(allergen)
                break

    safeIngredients = {f for f in ingredientsDict if f not in allergensMatched.values()}
    c = Counter(ingredientsGenerator())

    Part_1_Answer = 0

    for i in safeIngredients:
        Part_1_Answer += c[i]

    l = list(allergensMatched.keys())
    l.sort()
    canonical = []
    for k in l:
        canonical.append(allergensMatched[k])
        canonical.append(",")

    Part_2_Answer = "".join(canonical[:-1])

    return (Part_1_Answer, Part_2_Answer)