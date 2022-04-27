# from AOC_Lib.name import *

from collections import namedtuple
import functools
from operator import mul
from typing import Iterable, Generator


Ingredient = namedtuple("Ingredient", "name capacity durability flavor texture calories")
Recipe = tuple[int, int, int, int]

# TODO - there is definitely some speedup here, but it runs decently fast as is
#   possibly dynamic programming
#   probably (hill climb) optimization
#   certainly multi-processing
def generateAllCookies(ingredients: list[Ingredient], amt: int) -> Generator[tuple[Recipe, int], None, None]:

    if not ingredients:
        yield ((0,0,0,0), 0)
        return
    if amt == 0:
        yield ((0,0,0,0), 0)
        return

    remainder_ingredients = ingredients[1:]

    for i in range(0, amt+1):
        remainder_amt = amt - i
        for (cap, dur, fla, tex), cal in generateAllCookies(remainder_ingredients, remainder_amt):
            this_recipe = (
                cap + i*ingredients[0].capacity,
                dur + i*ingredients[0].durability,
                fla + i*ingredients[0].flavor,
                tex + i*ingredients[0].texture
            )
            this_cal = cal + i*ingredients[0].calories

            yield (this_recipe, this_cal)


def generateNonZeroScores(recipe_iterable: Iterable[Recipe]) -> Generator[int, None, None]:
    for recipe,_ in recipe_iterable:
        if any(map(lambda x: x <= 0, recipe)):
            continue
        yield functools.reduce(mul, recipe)


def teeMax(recipe_iterable: Iterable[Recipe], calorie_target:int = 500) -> tuple[int, int]:
    max_any = 0
    max_cal = 0
    for recipe,cal in recipe_iterable:
        if any(map(lambda x: x <= 0, recipe)):
            continue
        s = functools.reduce(mul, recipe)
        max_any = max(s, max_any)
        if cal == calorie_target:
            max_cal = max(s, max_cal)
    return max_any, max_cal


def y2015d15(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d15.txt"
    print("2015 day 15:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    # # sample input for debugging
    # lineList = [
    #     "Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8",
    #     "Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"
    # ]
    
    ingredients: list[Ingredient] = []

    # for multi line inputs
    for l in lineList:
        tokens = l.split(" ")
        ingredients.append(Ingredient(
            tokens[0][:-1],
            int(tokens[2][:-1]),
            int(tokens[4][:-1]),
            int(tokens[6][:-1]),
            int(tokens[8][:-1]),
            int(tokens[10])
        ))

    # print(ingredients)        

    # Part_1_Answer = max(generateNonZeroScores(generateAllCookies(ingredients, 100)))
    # Part_2_Answer = max(generateNonZeroScores(
    #     filter(lambda x: x[1] == 500, generateAllCookies(ingredients, 100))
    # ))
    Part_1_Answer, Part_2_Answer = teeMax(generateAllCookies(ingredients, 100))

    return (Part_1_Answer, Part_2_Answer)