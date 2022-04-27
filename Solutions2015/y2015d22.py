# from AOC_Lib.name import *

from collections import deque, namedtuple
from typing import Generator, Optional


# an effect
Effect_T = namedtuple("Effect_T", "name duration player_armor boss_damage player_mana")

# a spell
Spell_T = namedtuple("Spell_T", "name cost damage heal effect_index")

# an applied effect
AppliedEffect_t = namedtuple("AppliedEffect_T", "turns_remaining effect_index")

# game state
State_T = namedtuple("State_T", "player_health player_mana player_goes_next boss_health effects player_mana_spent")

EFFECTS = [
    Effect_T("Shield", 6, 7, 0, 0),
    Effect_T("Poision", 6, 0, 3, 0),
    Effect_T("Recharge", 5, 0, 0, 101),
]

SPELLS = [
    Spell_T("Magic Missile", 53, 4, 0, None),
    Spell_T("Drain", 73, 2, 2, None),
    Spell_T("Shield_s", 113, 0, 0, 0),
    Spell_T("Poison_s", 173, 0, 0, 1),
    Spell_T("Recharge_s", 229, 0, 0, 2),
]


class GameOver(Exception):
    def __init__(self, player_mana_spent: int, player_wins: int) -> None:
        super().__init__()
        self.player_mana_spent = player_mana_spent
        self.plyer_wins = player_wins


def getStartState(boss_health: int, player_health: int = 50, player_mana: int = 500) -> State_T:
    """Get the starting state based on boss parameters"""
    return State_T(player_health, player_mana, True, boss_health, [], 0)


def assertValidState(state: State_T) -> None:
    assert(state.player_health > 0)
    assert(state.player_mana >= 0)
    assert(state.player_goes_next is True or state.player_goes_next is False)
    assert(state.boss_health > 0)
    # check that no effect is applied twice
    assert(len(set(map(lambda x: x.effect_index, state.effects))) == len(state.effects))
    assert(all(map(lambda x: x.turns_remaining > 0, state.effects)))
    assert(all(map(lambda x: x.effect_index>= 0 and x.effect_index<=len(EFFECTS), state.effects)))
    assert(state.player_mana_spent >= 0)


def GenerateSuccessorStates(state: State_T, boss_damage: int) -> Generator[State_T, None, None]:
    """Generate the successor states to the current state"""

    assertValidState(state)

    p_health, p_mana, p_turn, b_health, old_effects, p_mana_spent = state
    p_armor = 0

    # apply effects
    updated_effects = []
    for applied_e in old_effects:
        time_remain = applied_e.turns_remaining
        effect_index = applied_e.effect_index
        assert(time_remain > 0)
        assert(effect_index >= 0 and effect_index < len(EFFECTS))
        effect = EFFECTS[effect_index]

        b_health -= effect.boss_damage

        if b_health <= 0:
            raise GameOver(p_mana_spent, True)

        p_mana += effect.player_mana

        if time_remain > 1:
            # the player has armor for this turn
            p_armor += effect.player_armor
            updated_effects.append(AppliedEffect_t(time_remain - 1, effect_index))
        # else:
        #   # this expired
        #   pass

    # now look at the options
    if p_turn == False:
        # this is a boss turn and the options are easy
        #   the boss attacks
        new_p_health = p_health - max(boss_damage - p_armor, 1)
        if new_p_health <= 0:
            raise GameOver(p_mana_spent, False)

        yield State_T(new_p_health, p_mana, True, b_health, updated_effects, p_mana_spent)
        return
    else:
        # player turn, consider all the spells we can cast
        can_cast_some_spell: bool = False

        for spell in SPELLS:
            if p_mana < spell.cost:
                # can't afford this spell
                continue

            if spell.effect_index is None:
                can_cast_some_spell = True
                new_p_mana_spent = p_mana_spent + spell.cost
                new_p_mana = p_mana - spell.cost
                new_p_health = p_health + spell.heal
                new_b_health = b_health - spell.damage
                yield State_T(new_p_health, new_p_mana, False, new_b_health, updated_effects, new_p_mana_spent)
            else:
                if spell.effect_index in map(lambda x: x.effect_index, updated_effects):
                    # can't re-cast this effect
                    continue
                can_cast_some_spell = True

                # this spell will create a new effect
                new_p_mana_spent = p_mana + spell.cost
                new_p_mana = p_mana - spell.cost
                new_effects = []
                new_effects.extend(updated_effects)
                new_effects.append(AppliedEffect_t(EFFECTS[spell.effect_index].duration, spell.effect_index))
                yield State_T(p_health, new_p_mana, False, b_health, new_effects, new_p_mana_spent)
        if not can_cast_some_spell:
            raise GameOver(p_mana_spent, False)
        return


def updateWinMana(new_val: int, old_val: Optional[int]) -> int:
    if old_val is None:
        print(f"Found candidate for win: {new_val}")
        return new_val
    elif new_val < old_val:
        print(f"Found better candidate: {new_val}")
        return new_val
    return old_val


def printState(state: State_T):
    print("-- {} turn --".format("Player" if state.player_goes_next else "Boss"))
    print("- Player has {} hit points, ?? armor, {} mana".format(state.player_health, state.player_mana))
    print("- Player has {} hit points".format(state.boss_health))


def y2015d22(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d22.txt"
    print("2015 day 22:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    boss_health, boss_damage = map(lambda x: int(x.split(" ")[-1]), lineList)

    print(f"Boss Health {boss_health}, Boss Damage {boss_damage}")

    best_win_mana = None

    state_q = deque()
    state_q.append(getStartState(boss_health))
    
    while len(state_q) > 0:
        this_state: State_T = state_q.popleft()

        if this_state.boss_health <= 0:
            best_win_mana = updateWinMana(this_state.player_mana_spent, best_win_mana)
            continue
        if this_state.player_health <= 0:
            raise RuntimeError("This should be unreachable")

        assertValidState(this_state)
        
        if best_win_mana is not None and this_state.player_mana_spent > best_win_mana:
            # this will be no better so prune
            continue
        
        try:
            state_q.extend(GenerateSuccessorStates(this_state, boss_damage))
        except GameOver as goe:
            if goe.plyer_wins:
                best_win_mana = updateWinMana(goe.player_mana_spent, best_win_mana)

    Part_1_Answer = best_win_mana

    try:
        assert(Part_1_Answer != 536)
        assert(Part_1_Answer > 400)
        assert(Part_1_Answer > 373)
        assert(Part_1_Answer != 367)
    except AssertionError:
        print("Our guess was: {}".format(Part_1_Answer))
        raise

    return (Part_1_Answer, Part_2_Answer)