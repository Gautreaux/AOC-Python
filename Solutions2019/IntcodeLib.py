
import asyncio
from enum import IntEnum, unique
import itertools
from operator import add, mul
from typing import Iterable, Optional


@unique
class OpCode(IntEnum):
    """Enum for all supported op codes"""
    ADD = 1,
    MUL = 2,
    INPUT = 3,
    OUTPUT = 4,
    JIT = 5,
    JIF = 6,
    LE = 7,
    EQ = 8,
    DONE = 99,

    def qtyParameters(self) -> int:
        """Return the number of parameters associated with this OpCode"""
        if self == OpCode.ADD:
            return 3
        elif self == OpCode.MUL:
            return 3
        elif self == OpCode.INPUT:
            return 1
        elif self == OpCode.OUTPUT:
            return 1
        elif self == OpCode.DONE:
            return 0
        elif self == OpCode.JIT:
            return 2
        elif self == OpCode.JIF:
            return 2
        elif self == OpCode.LE:
            return 3
        elif self == OpCode.EQ:
            return 3
        else:
            # unreachable?
            raise RuntimeError("Illegal op code: {} ({})".format(self, self.value))


@unique
class ParameterMode(IntEnum):
    """Enum for all parameter modes"""
    POSITION = 0,
    IMMEDIATE = 1,


class IntcodeProgram():
    """A class representing a intcode program"""

    def __init__(self, iterable):
        self._instr = list(iterable)

    def __iter__(self):
        return iter(self._instr)


class ProgramDone(Exception):
    """Raised when the program encounters a done instruction"""
    pass


class ProgramCrashed(Exception):
    """Raised when the program encounters a crash"""
    pass


class UnrecognizedOpCode(Exception):
    """Raised when the program encounters an unrecognized op code"""
    pass


class UnrecognizedParameterMode(Exception):
    """Raise if the parameter mode is not recognized"""
    pass


class IntcodeRunner():
    """A class for running intcode programs"""

    def __init__(self, 
        program: IntcodeProgram, 
        in_q: Optional[asyncio.Queue] = None, 
        out_q: Optional[asyncio.Queue] = None,
    ) -> None:
        self._instructionCounter = 0
        self._memory = list(program)
        self._isTerminal = False
        self._cycles = 0

        self.debug = False

        self._input_q = in_q if in_q is not None else asyncio.Queue()
        self._output_q = out_q if out_q is not None else asyncio.Queue()
        self._out_sema = asyncio.Semaphore(0)

    def getInputQ(self) -> asyncio.Queue:
        """Get the input Q for this execution"""
        return self._input_q

    def getOutputQ(self) -> asyncio.Queue:
        """Get the output Q for this execution"""
        return self._output_q

    def terminated(self) -> bool:
        """Return true if the program has run and is done (or crashed)"""
        return self._isTerminal

    def _advanceInstrCounter(self, op_code):
        """Logic for advancing the instruction pointer"""
        self._instructionCounter += (op_code.qtyParameters() + 1)

    async def _bin_op(self, op_code: OpCode, p_modes: tuple[ParameterMode, ...]) -> None:
        """Basic binary operators, all with 3 parameters"""
        if op_code == OpCode.ADD:
            operator = add
        elif op_code == OpCode.MUL:
            operator = mul
        elif op_code == OpCode.LE:
            # from operator import le
            #   returns true and false vs 1 and 0
            operator = (lambda x, y: 1 if x < y else 0)
        elif op_code == OpCode.EQ:
            operator = (lambda x, y: 1 if x == y else 0)
        else:
            raise RuntimeError("Bad op code for binary operation: {}".format(op_code))

        val_a, val_b = self._readParameters(p_modes[:2])
        out_val = operator(val_a, val_b)
        self._setModeAware(self._instructionCounter + 3, out_val, p_modes[2])
        self._advanceInstrCounter(op_code)

    async def _input_op(self, op_code: OpCode, p_modes: tuple[ParameterMode, ...]):
        """Basic input operator"""
        if p_modes[0] != ParameterMode.POSITION:
            raise RuntimeError("IDK")
        in_val = await self._input_q.get()
        self._input_q.task_done()
        if self.debug:
            print(f"READ in value: {in_val}")
        self.setAddr(self.readAddr(self._instructionCounter + 1), in_val)
        self._advanceInstrCounter(op_code)

    async def _jmp_op(self, op_code: OpCode, p_modes: tuple[ParameterMode, ...]):
        """Jump operators"""

        if op_code == OpCode.JIT:
            operator = lambda x : x != 0
        elif op_code == OpCode.JIF:
            operator = lambda x : x == 0

        val_a, val_b = self._readParameters(p_modes[:2])

        if operator(val_a):
            self._instructionCounter = val_b
        else:
            self._advanceInstrCounter(op_code)

    async def _output_op(self, op_code: OpCode, p_modes: tuple[ParameterMode, ...]):
        """Basic output operator"""
        out_val = self._readModeAware(self._instructionCounter + 1, p_modes[0])
        if self.debug:
            print(f"OUT value: {out_val}")
        await self._output_q.put(out_val)
        self._out_sema.release()
        self._advanceInstrCounter(op_code)

    async def _execOneCycle(self) -> None:
        """Run one cycle"""
        op_code, p_modes = self._readOpCode()

        if op_code == OpCode.ADD:
            await self._bin_op(op_code, p_modes)
        elif op_code == OpCode.MUL:
            await self._bin_op(op_code, p_modes)
        elif op_code == OpCode.INPUT:
            await self._input_op(op_code, p_modes)
        elif op_code == OpCode.OUTPUT:
            await self._output_op(op_code, p_modes)
        elif op_code == OpCode.JIT:
            await self._jmp_op(op_code, p_modes)
        elif op_code == OpCode.JIF:
            await self._jmp_op(op_code, p_modes)
        elif op_code == OpCode.LE:
            await self._bin_op(op_code, p_modes)
        elif op_code == OpCode.EQ:
            await self._bin_op(op_code, p_modes)
        elif op_code == OpCode.DONE:
            raise ProgramDone()
        else:
            raise UnrecognizedOpCode(op_code)

    def _readOpCode(self) -> tuple[OpCode, tuple[ParameterMode, ...]]:
        v = self.readAddr(self._instructionCounter)

        op_code = OpCode(v % 100)

        s = reversed(str(v))
        # remove the first two
        try:
            next(s)
            next(s)
        except StopIteration:
            pass

        p_mode_gen = itertools.chain(map(lambda x: ParameterMode(int(x)), s), itertools.repeat(ParameterMode(0)))
        p_modes = tuple(itertools.islice(p_mode_gen, op_code.qtyParameters()))
        return (op_code, p_modes)

    def _readParameters(self, p_modes: tuple[ParameterMode,...]) -> tuple[int, ...]:
        """Read all the parameters according to mode"""
        return tuple(map(
            (lambda x: self._readModeAware(self._instructionCounter + x + 1, p_modes[x])),
            range(len(p_modes))
        ))

    def _readModeAware(self, addr: int, p_mode: ParameterMode) -> int:
        """Read interpreting `addr` according to `mode`"""
        if p_mode == ParameterMode.POSITION:
            return self.readAddr(self.readAddr(addr))
        elif p_mode == ParameterMode.IMMEDIATE:
            return self.readAddr(addr)
        else:
            raise UnrecognizedParameterMode(p_mode)

    def _setModeAware(self, addr:int, val: int, p_mode: ParameterMode) -> int:
        """Set the `val` at `addr` according to `p_mode`"""
        if p_mode == ParameterMode.POSITION:
            return self.setAddr(self.readAddr(addr), val)
        elif p_mode == ParameterMode.IMMEDIATE:
            raise RuntimeError("This will never happen - 2019d5")
        else:
            raise UnrecognizedParameterMode(p_mode)

    def readAddr(self, addr:int) -> int:
        """Return the value stored at `addr`"""
        return self._memory[addr]

    def setAddr(self, addr:int, val: int) -> int:
        """Set the value stored at `addr` and return the value"""
        assert(isinstance(val, int))
        self._memory[addr] = val
        return val

    async def run(self):
        """Run cycles until complete"""
        while True:
            try:
                await self._execOneCycle()
                self._cycles += 1
            except ProgramDone:
                self._isTerminal = True
                # free the q if it is listenting
                self._out_sema.release()
                return
            except Exception:
                self.printStackFrame()

                self._isTerminal = True
                self._out_sema.release()
                raise

    async def _push_inputs(self, iterable: Iterable):
        """CO-RO to push the contents of iterable to the input"""
        # TODO - this may block a clean exit but whatever
        for f in iterable:
            assert(isinstance(f, int))
            await self._input_q.put(f)

    async def _collect_output(self):
        """CO-RO to collect the output while a program is running"""
        outputs = []
        while True:
            await self._out_sema.acquire()

            if self._isTerminal:
                while not self._output_q.empty():
                    outputs.append(self._output_q.get_nowait())
                return outputs
            else:
                try:
                    outputs.append(self._output_q.get_nowait())
                    self._output_q.task_done()
                except asyncio.QueueEmpty:
                    pass  

    def run_sync(self, inputs: Optional[Iterable] = None) -> list[str]:
        """Run until complete"""
        futures = []

        if inputs:
            futures.append(self._push_inputs(inputs))
        futures.append(self._collect_output())
        futures.append(self.run())

        f = asyncio.gather(*futures)
        v = asyncio.get_event_loop().run_until_complete(f)
        return v[1]

    def printStackFrame(self):
        print(f"=================")
        print("Progam is done? ", self.terminated())
        print("Memory is up to: ", len(self._memory))
        print(f"Cycles: ", self._cycles)
        print("Instruction Counter: ", self._instructionCounter)
        x = self._instructionCounter
        print("Memory region:", self._memory[x: x+8])
        print(f"=================")