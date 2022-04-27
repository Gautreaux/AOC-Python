from enum import IntEnum, unique
from typing import Any, Generator
from .IntcodeLib import *

def get2dHash(pos):
    return hash(pos[0]*10000+pos[1])


_GRID_DIM_X = 40
_GRID_DIM_Y = 25


@unique
class RenderChars(IntEnum):
    BLANK = 0,
    WALL = 1,
    BLOCK = 2,
    PADDLE = 3,
    BALL = 4,

    def render(self) -> str:
        return ({
            0: " ",
            1: "█",
            2: "÷",
            3: "_",
            4: "·",
        }[self.value])


@unique
class GameErrors(IntEnum):
    """words-based description of the game error conditions"""
    NONE = 0,
    MULTIPLE_BALLS = 1,
    MULTIPLE_PADDLES = 2,
    GAME_OVER = 16,
    NO_BLOCKS = 32,

    @classmethod
    def printErrorMaskDescription(cls, val:int):
        """Print words description of the error mask"""
        to_print = []
        for e in cls:
            if e == cls.NONE:
                continue
            if e.value & val:
                to_print.append(e.name)
        print("{:08b}: <{}>".format(val, ",".join(to_print)))


@unique
class JoystickPosition(IntEnum):
    NEUTRAL = 0,
    LEFT = -1,
    RIGHT = 1


def buildBlankGrid(init_value: Any = 0, x: int = _GRID_DIM_X, y: int = _GRID_DIM_Y) -> list[list[Any]]:
    to_return = [None]*y
    for i in range(y):
        to_return[i] = ([init_value]*x)
    return to_return


class GameState():
    def __init__(self):

        self._screen_grid = buildBlankGrid(RenderChars.BLANK)
        self._seven_seg_value = -1

        self._ball_pos_candidate = set()
        self._paddle_pos_candidate = set()
        self._num_blocks = 0

    def sendCommand(self):
        self.draw()
        i = input("Move: ") 
        if(i == 'l'):
            return -1
        elif(i == 'r'):
            return 1
        elif(i == ""):
            return 0
        else:
            return self.draw()

    def getBallPos(self) -> tuple[int, int]:
        """Returns the ball pos, raises an exception if multiple/none exist"""
        if len(self._ball_pos_candidate) == 1:
            return next(iter(self._ball_pos_candidate))
        else:
            raise RuntimeError(f"Total {len(self._ball_pos_candidate)} ball positions found")

    def getPaddlePos(self) -> tuple[int, int]:
        """Returns the paddle pos, raises an exception if multiple/none exist"""
        if len(self._paddle_pos_candidate) == 1:
            return next(iter(self._paddle_pos_candidate))
        else:
            raise RuntimeError(f"Total {len(self._paddle_pos_candidate)} paddle positions found")

    def getErrorMask(self) -> int:
        """Returns a bitmask of game error descriptors"""
        to_return = 0

        pp = None
        try:
            pp = self.getPaddlePos()
        except RuntimeError:
            to_return |= GameErrors.MULTIPLE_PADDLES
        
        bp = None
        try:
            bp = self.getBallPos()
        except RuntimeError:
            to_return |= GameErrors.MULTIPLE_BALLS

        if not ((pp is None) or (bp is None)):
            if pp[1] == bp[1]:
                # the ball is on the same y level as the paddle
                # this is game over
                to_return |= GameErrors.GAME_OVER
        
        if self._num_blocks == 0:
            to_return |= GameErrors.NO_BLOCKS
        
        return to_return

    @property
    def score(self) -> int:
        """return the score"""
        return self._seven_seg_value

    def draw(self):
        """Print the current board state to the console"""
        print("Score: {: 6d}".format(self._seven_seg_value))
        for row in self._screen_grid:
            print("".join(map(lambda x: x.render(), row)))

    def receiveCommandTriple(self, c: tuple[int, int, int]):
        """Process a triple to update the game state"""
        x_value, y_value, tile_id = c

        if((x_value == -1) and (y_value == 0)):
            self._seven_seg_value = tile_id
            return
        
        assert(x_value >= 0)
        assert(y_value >= 0)

        new = RenderChars(tile_id)
        old: RenderChars  = self._screen_grid[y_value][x_value]
        self._screen_grid[y_value][x_value] = new

        p = (x_value, y_value)

        if old == RenderChars.BLOCK:
            self._num_blocks -= 1
        elif old == RenderChars.PADDLE:
            self._paddle_pos_candidate.remove(p)
        elif old == RenderChars.BALL:
            self._ball_pos_candidate.remove(p)
       
        if new == RenderChars.BLOCK:
            self._num_blocks += 1
        elif new == RenderChars.PADDLE:
            self._paddle_pos_candidate.add(p)
        elif new == RenderChars.BALL:
            self._ball_pos_candidate.add(p)

    @property
    def num_blocks(self):
        """Number of blocks left in the game"""
        return self._num_blocks


def tuplesFromOutput(out_q: asyncio.Queue) -> Generator[tuple[int, int, int], None, None]:
    """Generate the tuples from the queue"""

    if out_q.qsize() % 3 != 0:
        print("[WARNING]: the size is {} and not a multiple of 3. Remaining items will be left.".format(out_q.qsize()))
    
    while out_q.qsize() >= 3:
        a = out_q.get_nowait()
        b = out_q.get_nowait()
        c = out_q.get_nowait()
        yield (a,b,c)


def runTillBlocked(
    io_event: asyncio.Event,
    run_task: asyncio.Task,
    loop: asyncio.AbstractEventLoop):
    """Run `runner` in `loop` until blocked for i/o
        or the program exits
    """

    wait_task = loop.create_task(io_event.wait())

    done, pending = loop.run_until_complete(asyncio.wait(
        [wait_task, run_task], return_when=asyncio.FIRST_COMPLETED
    ))

    if (wait_task in pending):
        # the runner has terminated so cleanup
        wait_task.cancel()

    # print("*-*-*-*-*-*-*-*-*-*-*-*")
    # print(done)
    # print(pending)
    # print("*-*-*-*-*-*-*-*-*-*-*-*")


def y2019d13(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d13.txt"
    print("2019 day 13:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    prog = IntcodeProgram(map(int, lineList[0].split(",")))

    #part 1
    gameState = GameState()

    runner = IntcodeRunner(prog)
    # runner.debug = True

    outputs = runner.run_sync()

    assert(len(outputs) % 3 == 0)

    try:
        outputs = iter(outputs)

        while True:
            a = next(outputs)
            b = next(outputs)
            c = next(outputs)
            gameState.receiveCommandTriple((a,b,c))
    except StopIteration:
        pass

    Part_1_Answer = gameState.num_blocks
    
    print(f"Part 1 Answer was: {Part_1_Answer}")

    #==========================

    gameState = GameState()

    runner = IntcodeRunner(prog)
    runner.setAddr(0, 2)

    loop = asyncio.get_event_loop()
    runner_task = loop.create_task(runner.run())

    runTillBlocked(runner.getIOEvent(), runner_task, loop)

    for t in tuplesFromOutput(runner.getOutputQ()):
        gameState.receiveCommandTriple(t)

    print(f"Start State: ")
    gameState.draw()

    for i in itertools.count():

        bp_x = gameState.getBallPos()[0]
        pp_x = gameState.getPaddlePos()[0]

        if bp_x == pp_x:
            runner.getInputQ().put_nowait(JoystickPosition.NEUTRAL.value)
        elif bp_x < pp_x:
            runner.getInputQ().put_nowait(JoystickPosition.LEFT.value)
        else:
            runner.getInputQ().put_nowait(JoystickPosition.RIGHT.value)

        # runner.getInputQ().put_nowait(0)

        runTillBlocked(runner.getIOEvent(), runner_task, loop)

        for t in tuplesFromOutput(runner.getOutputQ()):
            gameState.receiveCommandTriple(t)

        # print(f"After {i} turns:")
        # gameState.draw()

        if(i % 250 == 0):
            print(f"After {i} turns: {gameState.num_blocks} blocks remain")

        em = gameState.getErrorMask()
        if em != GameErrors.NONE:
            if em & GameErrors.NO_BLOCKS.value:
                pass
            else:
                print(f"Game detected errors after {i} turns")
                gameState.draw()
                GameErrors.printErrorMaskDescription(em)
                runner_task.cancel()
                break

        if runner.terminated():
            print(f"Runner has terminated: final score is {gameState.score}")
            Part_2_Answer = gameState.score
            break

        # sleep(1)

    # assert(Part_1_Answer != 399)
    # assert(Part_2_Answer > 15694)

    return (Part_1_Answer, Part_2_Answer)
