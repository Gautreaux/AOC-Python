
import multiprocessing
from typing import Dict, List

from cacheManager import SolutionNotStarted, SolutionType, getDateCodeCachedSolution, getDateCodeCurrentSolution, isCacheValid, runDayWrapper
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
    "y2015d1" : (280, 1797),
    "y2015d2" : (1588178, 3783758),
    "y2015d3" : (2565, 2639),
    "y2015d4" : (117946, 3938038),
    "y2015d5" : (236, 51),
    "y2015d6" : (377891, 14110788),
    "y2015d9" : (117, 909),
    "y2015d12" : (111754, 65402),
    "y2015d13" : (709, 668),
    "y2015d17" : (4275, 4),
    "y2015d19" : (535, object()),
    "y2016d1" : (252, 143),
    "y2016d2" : ("65556", "CB779"),
    "y2016d3" : (862, 1577),
    "y2016d4" : (409147, 991),
    "y2016d5" : ("4543c154", "1050cbbd"),
    "y2016d6" : ("tsreykjj", "hnfbujie"),
    "y2016d7" : (105, 258),
    "y2016d9" : (183269, 11317278863),
    "y2016d10" : (118, 143153),
    "y2016d12" : (318020, 9227674),
    "y2016d13" : (96, 1358),
    "y2016d14" : (15168, 20864),
    "y2016d15" : (16824, 3543984),
    "y2016d16" : ("10100101010101101", "01100001101101001"),
    "y2016d17" : ("RLDRUDRDDR", object()),
    "y2016d23" : (12624, object()),
    "y2016d24" : (500, 748),
    "y2017d1" : (1047, 982),
    "y2017d2" : (36766, 261),
    "y2017d3" : (430, 312453),
    "y2017d4" : (455, 186),
    "y2017d5" : (342669, 25136209),
    "y2017d7" : ("veboyvy", 749),
    "y2017d8" : (3880, 5035),
    "y2017d12" : (239, 215),
    "y2017d13" : (1840, 3850260),
    "y2017d15" : (597, 303),
    "y2017d17" : (1914, 41797835),
    "y2018d1" : (578, 82516),
    "y2018d2" : (6723, "prtkqyluiusocwvaezjmhmfgx"),
    "y2018d5" : (10888, 6952),
    "y2018d14" : ("1617111014", 20321495),
    "y2019d1" : (3434390, 5148724),
    "y2019d2" : (3101878, 8444),
    "y2019d3" : (232, 6084),
    "y2019d4" : (931, 609),
    "y2019d5" : (15386262, 10376124),
    "y2019d6" : (273985, 460),
    "y2019d7" : (14902, 6489132),
    "y2019d8" : (2684, "YGRYZ"),
    "y2019d9" : (3518157894, 80379),
    "y2019d10" : (296, 204),
    "y2019d11" : (1747, "ZCGRHKLB"),
    "y2019d12" : (14780, 279751820342592),
    "y2019d13" : (335, object()),
    "y2019d14" : (178154, 6226152),
    "y2019d16" : (84970726, object()),
    "y2019d18" : (5198, 1736),
    "y2020d1" : (805731, 192684960),
    "y2020d2" : (517, 284),
    "y2020d3" : (191, 1478615040),
    "y2020d4" : (230, 156),
    "y2020d5" : (874, 594),
    "y2020d6" : (6714, 3435),
    "y2020d7" : (119, 155802),
    "y2020d8" : (1134, 1205),
    "y2020d9" : (373803594, 51152360),
    "y2020d10" : (1836, 43406276662336),
    "y2020d11" : (2310, 2074),
    "y2020d12" : (1956, 126797),
    "y2020d13" : (3385, 600689120448303),
    "y2020d14" : (15403588588538, 3260587250457),
    "y2020d15" : (1111, 48568),
    "y2020d16" : (21996, 650080463519),
    "y2020d17" : (247, 1392),
    "y2020d18" : (6923486965641, 70722650566361),
    "y2020d19" : (248, 381),
    "y2020d20" : (17148689442341, 2009),
    "y2020d21" : (2302, "smfz,vhkj,qzlmr,tvdvzd,lcb,lrqqqsg,dfzqlk,shp"),
    "y2020d22" : (32272, 33206),
    "y2020d23" : (34952786, 505334281774),
    "y2020d24" : (339, 3794),
    "y2020d25" : (181800, None),
    "y2021d1" : (1301, 1346),
    "y2021d2" : (1698735, 1594785890),
    "y2021d3" : (741950, 903810),
    "y2021d4" : (29440, 13884),
    "y2021d5" : (8111, 22088),
    "y2021d6" : (386755, 1732731810807),
    "y2021d7" : (349769, 99540554),
    "y2021d8" : (409, 1024649),
    "y2021d9" : (545, 950600),
    "y2021d10" : (442131, 3646451424),
    "y2021d11" : (1661, 334),
}


def getCachedSolutionState(dateCode : str) -> int:
    answers = getDateCodeCurrentSolution(dateCode)
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
    try:
        for i in range(2):
            if knownAnswers[i] == answers[i]:
                stars += 1
    except Exception:
        stars = 0

    return [SOLUTION_INCORRECT, ONE_STAR, TWO_STAR][stars]

# TODO - finalize
def checkSolutionListMultiProcess(dateCodeList : List[str], timeout_s: int = 30) -> List[SolutionType]:
    results = {}
    toMultiProcess = []
    for dateCode in dateCodeList:
        if isCacheValid(dateCode):
            results[dateCode] = getDateCodeCachedSolution(dateCode)
        else:
            toMultiProcess.append(dateCode)

    # do the multiprocessing
    with multiprocessing.Pool(processes=5) as p:
       result = p.map_async(runDayWrapper, toMultiProcess, chunksize=1)

       r = result.get(timeout_s)
       print(r)


    # collect the results


    # reformat appropriately

    # return
    pass