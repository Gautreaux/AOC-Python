
from .IntcodeLib import *

import asyncio
from collections import defaultdict, deque, namedtuple
from enum import IntEnum, unique
from typing import Generator, Optional


RobotPosition = namedtuple("RobotPosition", "x y")
SearchState = namedtuple("SearchState", "position parent")

@unique
class MovementCommand(IntEnum):
    NORTH = 1,
    SOUTH = 2,
    WEST = 3,
    EAST = 4,

    def apply(self, pos: RobotPosition) -> RobotPosition:
        """Apply this movement to position and return new position"""
        if self == MovementCommand.NORTH:
            return RobotPosition(pos.x, pos.y+1)
        elif self == MovementCommand.SOUTH:
            return RobotPosition(pos.x, pos.y-1)
        elif self == MovementCommand.WEST:
            return RobotPosition(pos.x-1, pos.y)
        elif self == MovementCommand.EAST:
            return RobotPosition(pos.x+1, pos.y)
        else:
            raise NotImplementedError(self)

    def opposite(self) -> "MovementCommand":
        """Return the inverting movement"""
        if self == MovementCommand.NORTH:
            return MovementCommand.SOUTH
        elif self == MovementCommand.SOUTH:
            return MovementCommand.NORTH
        elif self == MovementCommand.WEST:
            return MovementCommand.EAST
        elif self == MovementCommand.EAST:
            return MovementCommand.WEST
        else:
            raise NotImplementedError(self)

    @classmethod
    def whatMoveAtoB(cls, 
        start_pos: RobotPosition, 
        end_pos: RobotPosition
    ) -> Optional["MovementCommand"]:
        """Return the movement to go from start_pos to end_pos
            or none if these are not adjacent
        """
        for f in cls:
            if f.apply(end_pos) == start_pos:
                return f.opposite()
        return None


@unique
class ResponseCommand(IntEnum):
    HIT_WALL = 0,
    MOVED_ONE_STEP = 1,
    MOVED_TO_O2 = 2,


@unique
class TileType(IntEnum):
    UKN = 0,
    CLEAR = 1,
    O2_SYS = 2,
    WALL = 3,

    def render(self) -> str:
        return ({
            0 : "?",
            1 : " ",
            2 : "2",
            3 : "█"
        }[self.value])


class NoPathException(Exception):
    """Raised when no path is possible"""
    pass


class EnvSearchManager():
    """Stores/Manages Environment Representation"""

    def __init__(self, runner: IntcodeRunner) -> None:
        self._runner = runner
        self._loop = asyncio.get_event_loop()
        self._run_task = self._loop.create_task(self._runner.run())

        self._robot_pos: RobotPosition = RobotPosition(0,0)

        self._tiles = defaultdict(lambda: TileType.UKN)
        self._tiles[self._robot_pos] = TileType.CLEAR

        self._goal_pos = None


        # candidates for future exploration 
        #   effectively used like a stack to exploit locality
        self.candidates = []

        self._qty_clear_tiles = 0
        self._qty_wall_tiles = 0
    
    @property
    def hasFoundGoal(self) -> bool:
        """Return true iff found the goal position"""
        return self._goal_pos is not None
    
    @property
    def goalPosition(self) -> Optional[RobotPosition]:
        """Return the goal position"""
        return self._goal_pos

    @property
    def currentPos(self) -> RobotPosition:
        """Return the current position"""
        return self._robot_pos
    
    def getTileValue(self, position: RobotPosition) -> TileType:
        """Get the value we know is at the position"""
        return self._tiles[position]

    def _issueMovement(self, movement: MovementCommand) -> Optional[ResponseCommand]:
        """Issue the movement and return response code
            Returns None if the program terminated
        """

        self._runner.getInputQ().put_nowait(movement.value)

        wait_task = self._loop.create_task(self._runner.getIOEvent().wait())

        done, pending = self._loop.run_until_complete(asyncio.wait(
            [wait_task, self._run_task], return_when=asyncio.FIRST_COMPLETED
        ))

        if (wait_task in pending):
            wait_task.cancel()

        out_q = self._runner.getOutputQ()

        if out_q.qsize() == 0:
            return None
        elif out_q.qsize() > 1:
            raise RuntimeError("[ERROR] too much output produced")
        else:
            return ResponseCommand(out_q.get_nowait())

    def issueMovement(self, movement: MovementCommand) -> ResponseCommand:
        """Issue the movement, get response, update state, return response"""
        respose = self._issueMovement(movement)

        if respose is None:
            raise NotImplementedError("Program exited unexpectedly?: {}".format(self._runner.terminated()))
        
        np = movement.apply(self.currentPos)

        if respose == ResponseCommand.HIT_WALL:
            assert(self._tiles[np] in [TileType.UKN, TileType.WALL])
            self._tiles[np] = TileType.WALL
            self._qty_wall_tiles += 1
        elif respose == ResponseCommand.MOVED_ONE_STEP:
            assert(self._tiles[np] in [TileType.UKN, TileType.CLEAR])
            self._tiles[np] = TileType.CLEAR
            self._robot_pos = np
            self._qty_clear_tiles += 1
        elif respose == ResponseCommand.MOVED_TO_O2:
            assert(self._tiles[np] in [TileType.UKN, TileType.O2_SYS])
            assert(self.hasFoundGoal == False)
            self._tiles[np] = TileType.O2_SYS
            self._goal_pos = np
            self._robot_pos = np
        else:
            raise NotImplementedError()

        return respose

    def getPath(self, 
        start_position: RobotPosition, 
        goal_positions: Iterable[RobotPosition],
    ) -> tuple[RobotPosition, Iterable[MovementCommand]]:
        """Find a set of movements to go from start position to any goal position
            No guarantees about shortest path
            returns tuple
                final position
                movements
            optional flag to move to first ukn tile
        """
        gpl = set(goal_positions)

        if not gpl:
            raise NoPathException("No goal positions provided")

        pending = deque()
        pending.append(SearchState(start_position, None))

        parent_map: dict[RobotPosition, Optional[RobotPosition]] = {}

        # the found goal state
        found_pos: Optional[SearchState] = None 

        while (pending) and (not found_pos):
            this_state: SearchState = pending.popleft()
            this_pos: RobotPosition = this_state.position

            if this_pos in gpl:
                found_pos = this_state
                break
            if this_pos in parent_map:
                # already visited
                continue
            
            parent_map[this_pos] = this_state.parent

            # generate successors
            for m in MovementCommand:
                np = m.apply(this_pos)
                if np in parent_map:
                    continue
                tt = self.getTileValue(np)
                if tt not in [TileType.CLEAR, TileType.O2_SYS]:
                    continue
                pending.append(SearchState(np, this_pos))
        
        if not found_pos:
            raise NoPathException()
        
        pending = []

        e_pos = found_pos.position
        s_pos = found_pos.parent

        while s_pos is not None:
            pending.append(MovementCommand.whatMoveAtoB(s_pos, e_pos))
            e_pos = s_pos
            s_pos = parent_map[e_pos]
        return (found_pos.position, reversed(pending))

    
    def exploreTileValue(self, target_position: RobotPosition) -> TileType:
        """Get the tile value, moving the robot to explore if necessary
            Raises NoPathException if no neighbor of `target_position` is clear
        """

        if self.getTileValue(target_position) != TileType.UKN:
            return self.getTileValue(target_position)

        current_pos = self.currentPos

        out_pos_possible = map(lambda x: (x.apply(target_position)), MovementCommand)
        out_pos_candidate = filter(lambda x: (self.getTileValue(x) == TileType.CLEAR), out_pos_possible)

        out_pos_candidate, b = itertools.tee(out_pos_candidate)

        # print(f"Trying to explore tile {target_position}")
        # print(f"Starting at {current_pos}")
        # print(f"Possible goals are {set(b)}")

        end_pos, path = self.getPath(current_pos, out_pos_candidate)

        path, b = itertools.tee(path)
        # print(f"Found path ending at {end_pos} len {sum(1 for _ in b)}")

        # now figure out the last_step
        last_step = MovementCommand.whatMoveAtoB(end_pos, target_position)

        for op in path:
            if(self.issueMovement(op) == ResponseCommand.HIT_WALL):   
                raise RuntimeError("Hit a wall unexpectedly")

        self.issueMovement(last_step)    

        e = self.getTileValue(target_position)
        assert(e != TileType.UKN)
        return e

    def display(self) -> None:
        """Display what we know about the world to the console"""
        min_x = min(map(lambda t: t.x, self._tiles.keys()))
        max_x = max(map(lambda t: t.x, self._tiles.keys()))
        min_y = min(map(lambda t: t.y, self._tiles.keys()))
        max_y = max(map(lambda t: t.y, self._tiles.keys()))

        for y in range(max_y, min_y, -1):
            for x in range(min_x, max_x+1):
                if x == 0 and y == 0:
                    print("S", end="")
                elif x == self.currentPos.x and y == self.currentPos.y:
                    print("R", end="")
                else:
                    print(self.getTileValue(RobotPosition(x,y)).render(), end="")
            print("")

    def exploreNearby(self) -> None:
        """Explore some unknown tile, favoring nearby tiles"""

        r_pos = self.currentPos

        for step_dir in MovementCommand:
            new_pos = step_dir.apply(r_pos) 

            if self.getTileValue(new_pos) == TileType.UKN:
                self.candidates.append(new_pos)

        while self.candidates:
            new_pos = self.candidates.pop()
            if self.getTileValue(new_pos) == TileType.UKN:
                self.exploreTileValue(new_pos)
                return

    def findO2System(self) -> RobotPosition:
        """Find and return the position of the O2 System"""

        while not self.hasFoundGoal:
            self.exploreNearby()
        
        return self.goalPosition
    
    def exploreAll(self) -> None:
        """Explore all tiles"""

        while self.candidates:
            self.exploreNearby()

    def countDistanceFrom(self, position: RobotPosition) -> Generator[tuple[RobotPosition, int], None, None]:
        """Generate the distances from position to all other tiles"""
        visited = set()
        frontier = deque()

        frontier.append((position, 0))
        visited.add(position)

        while frontier:
            yield frontier[0]
            this_pos, this_depth = frontier.popleft()

            for m in MovementCommand:
                p = m.apply(this_pos)
                if p not in visited:
                    if self.getTileValue(p) in [TileType.CLEAR, TileType.O2_SYS]:
                        visited.add(p)
                        frontier.append((p, this_depth+1))


def y2019d15(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d15.txt"
    print("2019 day 15:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    prog = IntcodeProgram(map(int, lineList[0].split(",")))
    runner = IntcodeRunner(prog)

    manager = EnvSearchManager(runner)

    o2_pos = manager.findO2System()

    print(f"O2 is located at {o2_pos}")

    manager.display()

    print("==================")

    manager.exploreAll()
    manager.display()

    _,path = manager.getPath(RobotPosition(0,0), (o2_pos, ))

    Part_1_Answer = sum(1 for _ in path)

    print("Part 1 answer is: ", Part_1_Answer)

    Part_2_Answer = max(map(lambda x: x[1], manager.countDistanceFrom(o2_pos)))

    return (Part_1_Answer, Part_2_Answer)