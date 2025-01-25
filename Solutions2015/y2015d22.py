# from AOC_Lib.name import *

from collections import deque, namedtuple
import itertools
from typing import Generator, Optional


# Effectively _is_part_2
IS_HARD_MODE: bool = False

# an effect
Effect_T = namedtuple("Effect_T", "name duration player_armor boss_damage player_mana")

# a spell
Spell_T = namedtuple("Spell_T", "name cost damage heal effect")

# an applied effect
AppliedEffect_t = namedtuple("AppliedEffect_T", "turns_remaining effect")

# game state
State_T = namedtuple(
    "State_T",
    "player_health player_mana player_goes_next boss_health effects player_mana_spent",
)


Effect_Shield = Effect_T("Shield", 6, 7, 0, 0)
Effect_Poison = Effect_T("Poison", 6, 0, 3, 0)
Effect_Recharge = Effect_T("Recharge", 5, 0, 0, 101)


# List of all effects that can be applied
EFFECTS: list[Effect_T] = [Effect_Shield, Effect_Poison, Effect_Recharge]


# List of all spells that can be used
SPELLS: list[Spell_T] = [
    Spell_T("Magic Missile", 53, 4, 0, None),
    Spell_T("Drain", 73, 2, 2, None),
    Spell_T("Shield_s", 113, 0, 0, Effect_Shield),
    Spell_T("Poison_s", 173, 0, 0, Effect_Poison),
    Spell_T("Recharge_s", 229, 0, 0, Effect_Recharge),
]


def getStartState(
    boss_health: int, player_health: int = 50, player_mana: int = 500
) -> State_T:
    """Get the starting state based on boss parameters"""
    return State_T(
        player_health=player_health,
        player_mana=player_mana,
        player_goes_next=True,
        boss_health=boss_health,
        effects=[],
        player_mana_spent=0,
    )


def assertValidState(state: State_T) -> None:
    assert state.player_health > 0
    assert state.player_mana >= 0
    assert state.player_goes_next is True or state.player_goes_next is False
    assert state.boss_health > 0
    assert state.player_mana_spent >= 0
    # check that no effect is applied twice
    assert len(set(map(lambda x: x.effect, state.effects))) == len(state.effects)

    for e in state.effects:
        assertValidActiveEffect(e)


def assertValidActiveEffect(applied_effect: AppliedEffect_t) -> None:
    """Assert that this is a valid applied effect"""
    assert applied_effect.turns_remaining > 0
    assert applied_effect.effect in EFFECTS


def applyActiveEffects(state: State_T) -> State_T:
    """Apply the active effects to the state and return it
    the remaining time is updated and expired effects are removed
    """

    remaining_effects: list[Effect_T] = []

    boss_health_net_change = 0
    player_mana_net_change = 0

    for applied_effect in state.effects:
        assertValidActiveEffect(applied_effect)
        effect: Effect_T = applied_effect.effect

        # print("EFFECT: ", effect.name)

        boss_health_net_change -= effect.boss_damage
        player_mana_net_change += effect.player_mana

        if applied_effect.turns_remaining > 1:
            remaining_effects.append(
                AppliedEffect_t(
                    turns_remaining=applied_effect.turns_remaining - 1,
                    effect=applied_effect.effect,
                )
            )

    return State_T(
        player_health=state.player_health,
        player_mana=state.player_mana + player_mana_net_change,
        boss_health=state.boss_health + boss_health_net_change,
        player_goes_next=state.player_goes_next,
        effects=remaining_effects,
        player_mana_spent=state.player_mana_spent,
    )


def doBossAction(state: State_T, boss_damage: int) -> Generator[State_T, None, None]:
    """Generate all successor states based on a boss action"""
    assert state.player_goes_next == False

    # determine if the player has armor
    player_armor = 0
    for active_effect in state.effects:
        if active_effect.effect == Effect_Shield:
            player_armor += Effect_Shield.player_armor

    # the boss has one action which is to attack so this is easy
    #   always do minimum one damage with an attack
    player_net_health = -max((boss_damage - player_armor), 1)

    # print("Boss Hit ", player_net_health)

    yield State_T(
        player_health=state.player_health + player_net_health,
        player_mana=state.player_mana,
        player_goes_next=True,
        boss_health=state.boss_health,
        effects=state.effects,
        player_mana_spent=state.player_mana_spent,
    )


def doPlayerAction(state: State_T) -> Generator[State_T, None, None]:
    """Generate all the states based on any player action"""
    assert state.player_goes_next == True

    for spell in SPELLS:
        if spell.cost > state.player_mana:
            # spell is to expensive, skip
            continue

        # print("CAST:", spell.name)

        if spell.effect is None:
            # this is a straight up spell
            #   so we can just cast it
            # pass
            new_effects = state.effects
        else:
            if spell.effect in map(lambda x: x.effect, state.effects):
                # this effect is already applied
                continue
            new_effects = []
            new_effects.extend(state.effects)
            new_effects.append(
                AppliedEffect_t(
                    turns_remaining=spell.effect.duration,
                    effect=spell.effect,
                )
            )
        yield State_T(
            player_health=state.player_health + spell.heal,
            player_mana=state.player_mana - spell.cost,
            player_goes_next=False,
            boss_health=state.boss_health - spell.damage,
            effects=new_effects,
            player_mana_spent=state.player_mana_spent + spell.cost,
        )


def GenerateSuccessorStates(
    state: State_T, boss_damage: int
) -> Generator[State_T, None, None]:
    """Generate the successor states to the current state"""

    assertValidState(state)
    assert not (isStateTerminal(state))

    # printState(state)

    global IS_HARD_MODE
    if IS_HARD_MODE and state.player_goes_next:
        state = State_T(
            player_health=state.player_health - 1,
            player_mana=state.player_mana,
            player_goes_next=state.player_goes_next,
            boss_health=state.boss_health,
            effects=state.effects,
            player_mana_spent=state.player_mana_spent,
        )
        if isStateTerminal(state=state):
            return iter([state])

    state_after_effect = applyActiveEffects(state)

    if isStateTerminal(state_after_effect):
        return iter([state_after_effect])

    if state.player_goes_next:
        return doPlayerAction(state_after_effect)
    else:
        return doBossAction(state_after_effect, boss_damage)


def isStateTerminal(state: State_T) -> bool:
    """Return `True` iff this state is terminal and should not be continued"""
    if state.player_health <= 0:
        return True
    if state.boss_health <= 0:
        return True
    # if state.player_mana < min(map(lambda x: x.cost, SPELLS)):
    #     return True
    return False


def printState(state: State_T):
    print("-- {} turn --".format("Player" if state.player_goes_next else "Boss"))
    print(
        "- Player has {} hit points, ?? armor, {} mana".format(
            state.player_health, state.player_mana
        )
    )
    print("- Boss has {} hit points".format(state.boss_health))


def runGame(
    boss_health: int, boss_damage: int, player_health: int = 50, player_mana: int = 500
) -> int:
    """Run a game, starting with the player"""

    start_state = getStartState(
        boss_health=boss_health, player_health=player_health, player_mana=player_mana
    )

    print(
        "New Game: boss health {}, boss damage {}, player health {}, player mana {}".format(
            boss_health,
            boss_damage,
            player_health,
            player_mana,
        )
    )

    # just a really big number
    best_win_mana = 2**31

    state_q: deque[State_T] = deque()
    state_q.append(start_state)

    while len(state_q) > 0:
        this_state: State_T = state_q.popleft()
        # print(f"<{best_win_mana} remain {len(state_q)}> {this_state}")

        if this_state.boss_health <= 0:
            assert this_state.player_health > 0
            print("Found a win condition at:", this_state.player_mana_spent)
            best_win_mana = min(this_state.player_mana_spent, best_win_mana)
            continue
        if this_state.player_health <= 0:
            continue

        assertValidState(this_state)

        if best_win_mana < this_state.player_mana_spent:
            # we already have a better solution, so no need to explore here
            continue

        state_q.extend(GenerateSuccessorStates(this_state, boss_damage))

    assert best_win_mana != 2**31
    return best_win_mana


def guessSpellCast(v: int) -> list[int]:
    """Debugging utility, guess what spells were cast to make up a specific total mana spent"""
    options = list(map(lambda x: x.cost, SPELLS))

    print("  Options:", options)

    m = min(options)
    rounds = (v // m) + 1
    if rounds > 5:
        print(f"  WARNING: guess will take up to {rounds} rounds, this may be slow")

    for i in range(1, rounds + 1):
        for c in itertools.combinations_with_replacement(options, i):
            if sum(c) == v:
                return c


def y2015d22(inputPath=None):
    if inputPath == None:
        inputPath = "Input2015/d22.txt"
    print("2015 day 22:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    assert len(lineList) == 2
    boss_health, boss_damage = map(lambda x: int(x.split(" ")[-1]), lineList)

    # =============
    # Test Cases
    v = runGame(14, 8, 10, 250)
    e = sum([229, 113, 73, 173, 53])
    if e != v:
        print("Expected: {}, got {}".format(e, v))
        print("  Guess: {}".format(guessSpellCast(v)))
    assert e == v
    print(f"First Test Case OK")
    v = runGame(13, 8, 10, 250)
    e = sum([173, 53])
    if e != v:
        print("Expected: {}, got {}".format(e, v))
        print("  Guess: {}".format(guessSpellCast(e)))
    assert e == v
    print(f"Second Test Case OK")

    # =============

    Part_1_Answer = runGame(boss_health=boss_health, boss_damage=boss_damage)

    try:
        assert Part_1_Answer != 536
        assert Part_1_Answer > 400
        assert Part_1_Answer > 373
        assert Part_1_Answer != 367
    except AssertionError:
        print("Our guess was: {}".format(Part_1_Answer))
        raise

    global IS_HARD_MODE
    IS_HARD_MODE = True
    Part_2_Answer = runGame(boss_health=boss_health, boss_damage=boss_damage)

    return (Part_1_Answer, Part_2_Answer)
