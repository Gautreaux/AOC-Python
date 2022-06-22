

# year 2016 days 12, 23, 25
# structured similarly to IntCode (2019)

import asyncio
from collections import namedtuple, defaultdict
from typing import Iterable, Iterator, Union

AssemBunnyInstruction = namedtuple(
    "AssemBunnyInstruction", 
    "op arg1 arg2 is_toggled",
    defaults=(False,))


class LockedProgramException(Exception):
    """Raised when attempting to modify a locked program"""


class IllegalRegisterException(Exception):
    """Raised when attempting to read/write an invalid register"""


class UnrecognizedOperationException(Exception):
    """Raised when an unrecognized operation is attempted"""


class AssemBunnyProgram:
    """Program containing AssemBunny"""

    def __init__(self, iterable: Iterable[AssemBunnyInstruction], locked: bool = True):
        self._instructions = list(iterable)
        self._locked = locked

    @classmethod
    def parseCommand(cls, s: str) -> AssemBunnyInstruction:
        """Parse a single command"""
        tokens = s.split(" ")

        for i,t in enumerate(tokens,):
            try:
                tokens[i] = int(t)
            except:
                pass

        while len(tokens) < 3:
            tokens.append(None)

        return AssemBunnyInstruction(*tokens)

    @classmethod
    def fromStrs(cls, iterable: Iterable[str]) -> 'AssemBunnyProgram':
        """Build a AssemBunnyProgram from the list of strs"""
        a = map(cls.parseCommand, iterable)
        return AssemBunnyProgram(a)

    @property
    def locked(self) -> bool:
        """return `True` iff this program is locked"""
        return self._locked

    def lock(self) -> None:
        """Mark this program as locked and block any updates"""
        self._locked = True
    
    def unlock(self) -> None:
        """Unlock this program and allow updates"""

    def __iter__(self) -> Iterator[AssemBunnyInstruction]:
        return iter(self._instructions)

    def __getitem__(self, i: int) -> AssemBunnyInstruction:
        if i >= len(self._instructions) or i < 0:
            raise IndexError("Index {} out of range".format(i))
        return self._instructions[i]

    def __setitem__(self, i: int, instr: AssemBunnyInstruction) -> None:
        if i >= len(self._instructions) or i < 0:
            raise IndexError("Index {} out of range".format(i))
        if self.locked:
            raise LockedProgramException()
        self._instructions[i] = instr

    def copy(self) -> 'AssemBunnyProgram':
        """Return a copy of the AssemBunnyInstruction"""
        return AssemBunnyProgram(self._instructions, self._locked)


class AssemBunnyRunner:
    def __init__(self, program: AssemBunnyProgram) -> None:
        self._program = program
        self._output_q = asyncio.Queue()
        self._memory = defaultdict(int)
        self._prog_counter = 0
        self._is_done = False

    @property
    def output_q(self) -> asyncio.Queue():
        """Get a reference to the output queue"""
        return self._output_q

    def isValidRegister(self, register: str) -> bool:
        """Return `True` iff register is valid"""
        return register in "abcd"

    def _registerAccessWrapper(self, register: str) -> str:
        """Return the register if it is valid,
            otherwise throw IllegalRegisterException
        """
        try:
            if self.isValidRegister(register):
                return register
        except TypeError as ex:
            raise IllegalRegisterException(f"Illegal Register: {register}") from ex
        raise IllegalRegisterException(f"Illegal Register: {register}")

    def _unifiedMemAccess(self, register_or_value: Union[str, int]) -> int:
        """Unified memory access"""
        if isinstance(register_or_value, int):
            return register_or_value
        else:
            return self._memory[register_or_value]
            # return self._memory[self._registerAccessWrapper(register_or_value)]
    
    def getMemValue(self, register: str) -> int:
        """Get the value stored at a register"""
        return self._memory[self._registerAccessWrapper(register)]
        
    def setMemValue(self, register: str, value: int) -> int:
        """Set the value stored at a register
            and returns the newly set value
        """
        self._memory[self._registerAccessWrapper(register)] = value
        return value
    
    def inc(self, register: str) -> None:
        """Increment Register specified by `address`"""
        self._memory[self._registerAccessWrapper(register)] += 1
        self._prog_counter += 1

    def dec(self, register: str) -> None:
        """Decrement Register specified by `address`"""
        self._memory[self._registerAccessWrapper(register)] -= 1
        self._prog_counter += 1
    
    def cpy(self, register_or_value: Union[str, int], dest_register: str) -> None:
        """Copy the value (or value at register) into dest_register"""

        # if isinstance(register_or_value, int):
        #     self._memory[self._registerAccessWrapper(dest_register)] = register_or_value
        # else:
        #     self._memory[self._registerAccessWrapper(dest_register)] = self._memory[
        #         self._registerAccessWrapper(register_or_value),
        #     ]
        self.setMemValue(dest_register, self._unifiedMemAccess(register_or_value))
        self._prog_counter += 1

    def jnz(self, value: Union[int, str], y: Union[int, str]) -> None:
        """Jump if value is not zero."""
        if self._unifiedMemAccess(value) == 0:
            self._prog_counter += 1
        else:
            self._prog_counter += self._unifiedMemAccess(y)

    def tgl(self, offset: Union[int, str]) -> None:
        """Toggle the instruction specified by `value`"""

        raise NotImplementedError()

        pc_index = self._prog_counter + offset

        try:
            old_instr = self._program[pc_index]
        except IndexError:
            self._prog_counter += 1
            return
        
        if old_instr.op == "inc":
            new_op = "dec"
        elif old_instr.op == "dec":
            new_op = "inc"
        elif old_instr.op == "tgl":
            new_op = "inc"
        elif old_instr.op == "jnz":
            new_op = "cpy"
        elif old_instr.op == "cpy":
            new_op = "jnz"
        
        new_instr = AssemBunnyInstruction(new_op, old_instr.arg1, old_instr.arg2, True)
        self._program[pc_index] = new_instr
        self._prog_counter += 1

    async def _run_one_cycle(self) -> None:
        """Run One Cycle"""
        if self._is_done:
            return

        try:
            instr = self._program[self._prog_counter]
            # print(instr, self._memory)
        except IndexError:
            self._is_done = True
            return

        try:
            if instr.op == "inc":
                self.inc(instr.arg1)
            elif instr.op == "dec":
                self.inc(instr.arg1)
            elif instr.op == "cpy":
                self.cpy(instr.arg1, instr.arg2)
            elif instr.op == "jnz":
                self.jnz(instr.arg1, instr.arg2)
            elif instr.op == "tgl":
                self.tgl(instr.arg1)
            else:
                raise UnrecognizedOperationException(instr.op)
        except IllegalRegisterException:
            if instr.is_toggled:
                return
            else:
                raise
        
    async def run(self) -> None:
        """Run until complete"""
        self.printProgram()

        while not self._is_done:
            await self._run_one_cycle()
    
    def run_sync(self) -> None:
        """Run until complete, synchronous"""
        asyncio.get_event_loop().run_until_complete(self.run())

    def printProgram(self) -> None:
        """Print the current version of the program"""
        # debugging utility
        print("=== Program is: ===")
        for i in self._program:
            print(" ", i)
        print("===================")
