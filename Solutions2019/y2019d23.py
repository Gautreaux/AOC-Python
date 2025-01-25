import asyncio

from .IntcodeLib import IntcodeProgram, IntcodeRunner

from collections import defaultdict
from typing import Optional
from random import randint

# A shared lock for all queue pushes
#   Should not be necessary
#   but it costs nothing to be sure
_push_lock = asyncio.Lock()


async def PushRouter(
    q: asyncio.Queue,
    network_addresses: dict[int, asyncio.Queue],
    NAT: Optional["NAT"] = None,
):
    """Listen and construct the three-byte messages on q; send to the appropriate address
    When NAT is provided,
        pass any 255 packets to the NAT (part 2)
    when not provided,
        return the value
    """
    global _push_lock

    while True:
        address = await q.get()
        q.task_done()
        x_value = await q.get()
        q.task_done()
        y_value = await q.get()
        q.task_done()

        if address == 255:
            if NAT is None:
                # part 1
                print("Sending y value to address 255: {}".format(y_value))
                return y_value
            else:
                # part 2
                async with _push_lock:
                    NAT.in_q.put_nowait(x_value)
                    NAT.in_q.put_nowait(y_value)
                    continue

        if address not in network_addresses:
            raise RuntimeError(f"Unsupported network address: {address}")

        # use no-wait to prevent yielding the event loop
        #   and packets getting out of order
        # added a lock for good measure too
        async with _push_lock:
            network_addresses[address].put_nowait(x_value)
            network_addresses[address].put_nowait(y_value)
            if NAT is not None:
                NAT.transmissionOccurred()


async def RandomNegOne(runners: dict[int, IntcodeRunner]):
    """Randomly find blocked NICs and push instructions"""
    while True:
        await asyncio.sleep(0.05)
        async with _push_lock:
            for _ in range(5):
                i = randint(0, 49)
                if runners[i].isIOBlocked():
                    runners[i].getInputQ().put_nowait(-1)
                    break


class NAT:
    """Not Always Transmitting Controller"""

    def __init__(self, nic: dict[int, IntcodeRunner]) -> None:
        self._in_q = asyncio.Queue()

        # capture references to the running programs
        self._nic_dict = nic

        # for actually building an output
        self.last_push_y = None
        self.last_recv_x = None
        self.last_recv_y = None

        # used to track how many retries are in flight
        self._retry_tracker: dict[int, int] = {}
        self._reset_retry_tracker()

        # this event is set when `self.result` is ready
        self._done_event: asyncio.Event = asyncio.Event()
        self._result = None

        loop = asyncio.get_event_loop()
        self._recv_task = loop.create_task(self._NAT_recv())
        self._monitor_task = loop.create_task(self._NAT_monitor())

    def __del__(self):
        if not self._recv_task.done():
            self._recv_task.cancel()
        if not self._monitor_task.done():
            self._monitor_task.cancel()

    @property
    def in_q(self) -> asyncio.Queue:
        """Get the queue that the NAT is running on"""
        return self._in_q

    @property
    def result(self) -> Optional[int]:
        """Get the result, non-blocking"""
        return self._result

    def transmissionOccurred(self) -> None:
        """Notify that some network transmission occurred
        used to reset internal watchdogs in the NAT
        """
        self._reset_retry_tracker()

    def _reset_retry_tracker(self):
        """Reset the retry tracker"""
        for nic_id in range(50):
            self._retry_tracker[nic_id] = 5

    async def WaitForResult(self) -> int:
        """Block and wait for NAT to mark done, return the value"""
        await self._done_event.wait()
        return self.result

    async def _NAT_recv(self) -> None:
        """Receive function for NAT;
        Managed internally by the NAT
        """
        while True:
            x = await self._in_q.get()
            self._in_q.task_done()
            y = await self.in_q.get()
            self._in_q.task_done()
            self.last_recv_x = x
            self.last_recv_y = y
            self.transmissionOccurred()

    async def _unblock(self) -> None:
        """The NAT has decided the network is blocked, and thus shall unblock"""
        global _push_lock
        print(f"Unblocking via sending 0: {self.last_recv_x},{self.last_recv_y}")
        if self.last_recv_y == None:
            raise RuntimeError("Something is wrong")
        if self.last_push_y == self.last_recv_y:
            print(f"Found a repeated push of y =", self.last_recv_y)
            if self._result is None:
                self._result = self.last_recv_y
                self._done_event.set()
        async with _push_lock:
            self._nic_dict[0].getInputQ().put_nowait(self.last_recv_x)
            self._nic_dict[0].getInputQ().put_nowait(self.last_recv_y)
            self.last_push_y = self.last_recv_y
            self._reset_retry_tracker()

    async def _NAT_monitor(self) -> None:
        """Monitor function for NAT;
        Managed internally by the NAT
        """
        while True:
            await asyncio.sleep(0.1)
            to_pop = []
            for k, v in self._retry_tracker.items():
                runner = self._nic_dict[k]
                if runner.isIOBlocked():
                    if v == 0:
                        to_pop.append(k)
                    else:
                        runner.getInputQ().put_nowait(-1)
                        self._retry_tracker[k] -= 1
            for k in to_pop:
                self._retry_tracker.pop(k)

            if len(self._retry_tracker) == 0:
                await self._unblock()


def y2019d23(inputPath=None):
    if inputPath == None:
        inputPath = "Input2019/d23.txt"
    print("2019 day 23:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    prog = IntcodeProgram(map(int, lineList[0].split(",")))

    network_addresses = {}
    runners = {}

    loop = asyncio.get_event_loop()

    task_list = []

    for i in range(50):
        q = asyncio.Queue()
        network_addresses[i] = q
        q.put_nowait(i)
        runner = IntcodeRunner(prog, in_q=q)
        task_list.append(
            loop.create_task(PushRouter(runner.getOutputQ(), network_addresses))
        )
        runners[i] = runner
        task_list.append(loop.create_task(runner.run()))

    task_list.append(RandomNegOne(runners))

    done, pending = loop.run_until_complete(
        asyncio.wait(task_list, return_when=asyncio.FIRST_COMPLETED)
    )

    candidates = list(map(lambda x: x.result(), done))

    if len(candidates) <= 0:
        raise RuntimeError("This should be unreachable")
    elif len(candidates) > 1:
        print("WARN: Multiple part 1 answers found:", candidates)
    else:
        print(f"Part 1: {candidates[0]}")
    print(f"  done tasks: {done}")

    Part_1_Answer = candidates[0]

    # Part 2

    network_addresses: dict[int, asyncio.Queue] = {}
    nic_dict: dict[int, IntcodeRunner] = {}
    task_list = []

    nat = NAT(nic_dict)
    task_list.append(loop.create_task(nat.WaitForResult()))

    for i in range(50):
        q = asyncio.Queue()
        q.put_nowait(i)
        runner = IntcodeRunner(prog, in_q=q)
        network_addresses[i] = q
        nic_dict[i] = runner
        task_list.append(
            loop.create_task(PushRouter(runner.getOutputQ(), network_addresses, nat))
        )
        task_list.append(loop.create_task(runner.run()))

    done, pending = loop.run_until_complete(
        asyncio.wait(
            task_list,
            return_when=asyncio.FIRST_COMPLETED,
        )
    )

    if not task_list[0].done():
        print("WARN: The task that should have finished, didn't")

    candidates = list(map(lambda x: x.result(), done))

    if len(candidates) <= 0:
        raise RuntimeError("This should be unreachable")
    elif len(candidates) > 1:
        print("WARN: Multiple part 1 answers found:", candidates)
    else:
        print(f"Part 2: {candidates[0]}")
    print(f"  done tasks: {done}")

    Part_2_Answer = candidates[0]

    return (Part_1_Answer, Part_2_Answer)
