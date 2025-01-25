# from AOC_Lib.name import *

import asyncio
from asyncio.tasks import FIRST_COMPLETED

goalSet = {17, 61}

# amount to offset output queues to make them have unique ids
OUTPUT_OFFSET = 100000


async def someRobot(
    botId, inQ, doneQ, isOutput=False, lowOutQueue=None, highOutQueue=None
):
    while True:
        v1 = await inQ.get()
        v2 = await inQ.get()

        if isOutput:
            continue
        else:
            if {v1, v2} == goalSet:
                print(f"Comparision happened at target: {botId}")
                await doneQ.put(botId)

            await lowOutQueue.put(min(v1, v2))
            await highOutQueue.put(max(v1, v2))


async def thingy(lineList):
    Part_1_Answer = None
    Part_2_Answer = None

    # key value pair mapping
    #   botId to the requisite input queue
    queueDict = {}

    botIdSet = set()
    botData = {}

    # for multi line inputs
    for line in lineList:
        t = line.split(" ")
        if "value" in line:
            assert t[-2] == "bot"
            value = int(t[1])
            botId = int(t[-1])
            assert botId < OUTPUT_OFFSET

            if botId not in queueDict:
                queueDict[botId] = asyncio.Queue()
            await queueDict[botId].put(value)

            botIdSet.add(botId)
        else:
            assert "gives" in line

            sourceId = int(t[1])

            assert sourceId < OUTPUT_OFFSET
            botIdSet.add(sourceId)

            lowSinkId = int(t[6])
            if t[5] == "output":
                lowSinkId += OUTPUT_OFFSET
            else:
                assert lowSinkId < OUTPUT_OFFSET
                botIdSet.add(lowSinkId)

            highSinkId = int(t[-1])
            if t[-2] == "output":
                highSinkId += OUTPUT_OFFSET
            else:
                assert highSinkId < OUTPUT_OFFSET
                botIdSet.add(highSinkId)

            if lowSinkId not in queueDict:
                queueDict[lowSinkId] = asyncio.Queue()

            if highSinkId not in queueDict:
                queueDict[highSinkId] = asyncio.Queue()

            botData[sourceId] = (lowSinkId, highSinkId)

    taskList = []

    doneQ = asyncio.Queue()

    for botId in botIdSet:
        # if assert fails,
        #   bot is pushed to but never popped from
        assert botId in botData

        lowId, highId = botData[botId]

        t = asyncio.create_task(
            someRobot(
                botId,
                queueDict[botId],
                doneQ,
                False,
                queueDict[lowId],
                queueDict[highId],
            )
        )

        taskList.append(t)

    for t in taskList:
        asyncio.ensure_future(t)

    async def partOne():
        return await doneQ.get()

    async def partTwo():
        v0 = await queueDict[0 + OUTPUT_OFFSET].get()
        v1 = await queueDict[1 + OUTPUT_OFFSET].get()
        v2 = await queueDict[2 + OUTPUT_OFFSET].get()
        return v0 * v1 * v2

    Part_1_Answer, Part_2_Answer = await asyncio.gather(partOne(), partTwo())

    # cleanup
    for t in taskList:
        t.cancel()

    return (Part_1_Answer, Part_2_Answer)


def y2016d10(inputPath=None):
    if inputPath == None:
        inputPath = "Input2016/d10.txt"
    print("2016 day 10:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    Part_1_Answer, Part_2_Answer = asyncio.run(thingy(lineList))

    return (Part_1_Answer, Part_2_Answer)
