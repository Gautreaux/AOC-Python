# from AOC_Lib.name import *

from collections import namedtuple
from enum import IntEnum, unique
import itertools
from typing import Any, Generator, Optional


Item_T = namedtuple("ItemType", "name cost damage armor type")
Loadout_T = tuple[Item_T, Item_T, Item_T, Item_T]


@unique
class ItemType(IntEnum):
    WEAPON = (1,)
    ARMOR = (2,)
    RING = (4,)


ITEM_SHOP = [
    Item_T("Dagger", 8, 4, 0, ItemType.WEAPON),
    Item_T("Shortsword", 10, 5, 0, ItemType.WEAPON),
    Item_T("Warhammer", 25, 6, 0, ItemType.WEAPON),
    Item_T("Longsword", 40, 7, 0, ItemType.WEAPON),
    Item_T("Greataxe", 74, 8, 0, ItemType.WEAPON),
    Item_T("Leather", 13, 0, 1, ItemType.ARMOR),
    Item_T("Chainmail", 31, 0, 2, ItemType.ARMOR),
    Item_T("Splintmail", 53, 0, 3, ItemType.ARMOR),
    Item_T("Bandedmail", 75, 0, 4, ItemType.ARMOR),
    Item_T("Platemail", 102, 0, 5, ItemType.ARMOR),
    Item_T("Damage +1", 25, 1, 0, ItemType.RING),
    Item_T("Damage +2", 50, 2, 0, ItemType.RING),
    Item_T("Damage +3", 100, 3, 0, ItemType.RING),
    Item_T("Defense +1", 20, 0, 1, ItemType.RING),
    Item_T("Defense +2", 40, 0, 2, ItemType.RING),
    Item_T("Defense +3", 80, 0, 3, ItemType.RING),
    Item_T("NullRing", 0, 0, 0, ItemType.RING),
    Item_T("NullRing2", 0, 0, 0, ItemType.RING),
    Item_T("NullArmor", 0, 0, 0, ItemType.ARMOR),
]


def LoadoutGenerator(
    max_money: Optional[int] = None,
) -> Generator[Loadout_T, None, None]:
    """Generate all possible loadouts from the shop given the money we have"""

    a_list = [f for f in ITEM_SHOP if f.type == ItemType.ARMOR]
    w_list = [f for f in ITEM_SHOP if f.type == ItemType.WEAPON]
    r_list = [f for f in ITEM_SHOP if f.type == ItemType.RING]

    for w in w_list:
        for a in a_list:
            for r1, r2 in itertools.combinations(r_list, 2):
                items = (w, a, r1, r2)

                if max_money is None:
                    yield items
                else:
                    cost = sum(map(lambda x: x.cost, items))
                    if cost <= max_money:
                        yield items


# The algorithms do battle
#   thats a really funny joke for the few people who get it
def doesPlayerWinBattle(loadout: Loadout_T, boss_stats: tuple[int, int, int]) -> 0:

    player_health = 100
    player_damage = sum(map(lambda x: x.damage, loadout))
    player_armor = sum(map(lambda x: x.armor, loadout))

    boss_health, boss_damage, boss_armor = boss_stats

    for i in itertools.count(start=1):
        # player goes
        boss_health -= max(player_damage - boss_armor, 1)
        if boss_health <= 0:
            return True

        # boss goes
        player_health -= max(boss_damage - player_armor, 1)
        if player_health <= 0:
            return False


def y2015d21(inputPath=None):
    if inputPath == None:
        inputPath = "Input2015/d21.txt"
    print("2015 day 21:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    boss_stats = tuple(map(lambda x: int(x.split(" ")[-1]), lineList))

    all_loadouts = LoadoutGenerator()

    battles = map(
        lambda x: (
            x,
            doesPlayerWinBattle(x, boss_stats),
            sum(map(lambda i: i.cost, x)),
        ),
        all_loadouts,
    )

    a, b = itertools.tee(battles)

    winning_battles = filter(lambda x: x[1], a)
    losing_battles = filter(lambda x: (not x[1]), b)

    Part_1_Answer = min(map(lambda x: x[2], winning_battles))
    Part_2_Answer = max(map(lambda x: x[2], losing_battles))

    return (Part_1_Answer, Part_2_Answer)
