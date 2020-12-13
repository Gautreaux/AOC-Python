

from typing import Any, Dict, Tuple, Union

from cacheManager import SolutionNotStarted, SolutionType, getDateCodeCachedSolution
from main import FunctionImportError

# TODO - these should become an enum
ERROR_UKN = -1
SOLUTION_NOT_STARTED = 0
ONE_STAR = 1
TWO_STAR = 2
SOLUTION_INCORRECT = 3
SOLUTION_EXCEPTION = 4
SOLUTION_ANS_NOT_PROVIDED = 5

# stores all the solutions and their known values
solutionDict : Dict[str, SolutionType] = {
    
}


def getCachedSolutionState(dateCode : str) -> int:
    answers = getDateCodeCachedSolution(dateCode)
    if answers == SolutionNotStarted:
        return SOLUTION_NOT_STARTED
    elif answers == FunctionImportError:
        return ERROR_UKN
    elif answers == RuntimeError:
        return SOLUTION_EXCEPTION
    
    # we know the answer returned something
    if dateCode not in solutionDict:
        return SOLUTION_ANS_NOT_PROVIDED

    knownAnswers = solutionDict[dateCode]

    stars = 0
    for i in range(2):
        if knownAnswers[i] == answers[i]:
            stars += 1
    
    return [SOLUTION_INCORRECT, ONE_STAR, TWO_STAR][stars]

