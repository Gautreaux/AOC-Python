"""Core components of a Solution"""

from dataclasses import dataclass
from enum import Enum, unique
from typing import Any, Callable, Iterator, Optional, TypeVar
import re


# Regex for splitting a inheriting class into a date code
_solution_name_re = re.compile(r'^Solution_(\d{4})_(\d{2})$')

# Type var for covariance in annotations
_MappedType_T = TypeVar('_MappedType_T')

# Placeholder for an answer
Answer_T = Any

# Placeholder for a day's answer
AnswerPair_T = tuple[Answer_T, Answer_T]


@dataclass(frozen=True)
class DateCode:
    """Represents a Date Code"""
    year: int
    day: int

    @classmethod
    def get_latest(cls) -> 'DateCode':
        """Return the latest DateCode"""
        raise NotImplementedError()

    @classmethod
    def from_legacy_datecode(cls, date_code) -> 'DateCode':
        """Convert a y####d# code to a date code"""
        return cls(
            year=int(date_code[1:5]),
            day=int(date_code[6:]),
        )

    def to_legacy_datecode(self) -> str:
        """Format as a legacy date code and return"""
        return f"y{self.year}d{self.day}"


@unique
class InputType(Enum):
    AUTO = 0
    BYTES = 1
    FILE_PATH = 2


@dataclass(frozen=True)
class InputSpecification:
    """A method of specifying input"""

    input_type: InputType
    bytes_content: bytes = b''
    file_path: str = ''

    @classmethod
    def AUTO_Factory(cls) -> 'InputSpecification':
        return cls(input_type=InputType.AUTO)
    

class SolutionBase:
    """Base Implementation of a solution"""

    # Whenever a class inherits this one,
    #   we capture a reference in this object
    # This allows for the quick running of specific days
    #   as derivatives of this class
    _known_implementations: dict[DateCode, type['SolutionBase']] = {}

    def __init__(
        self,
        input_spec: InputSpecification = InputSpecification.AUTO_Factory(),
        date_code:Optional[DateCode] = None
    ) -> None:

        self.date_code: DateCode = date_code

        if self.date_code is None:
            self.date_code = self._infer_date_code()

        self._part_1_answer: Optional[Answer_T] = None
        self._part_2_answer: Optional[Answer_T] = None

        self._input: bytes = input_spec.bytes_content
        self._input_spec: InputSpecification = input_spec

        if input_spec.input_type == InputType.BYTES:
            pass
        elif input_spec.input_type == InputType.FILE_PATH:
            with open(input_spec.file_path, 'rb') as in_file:
                self._input = in_file.read()
        elif input_spec.input_type == InputType.AUTO:
            f_name = f"Input{self.date_code.year}/d{self.date_code.day}.txt"
            with open(f_name, 'rb') as in_file:
                self._input = in_file.read()
        else:
            raise TypeError(f"Unsupported Type: {input_spec.input_type.name}")

        self.__post_init__()

    def __post_init__(self) -> None:
        """
        Called once at the end of `__init__`
        
        Subclasses should probably not override `__init__` and instead
          prefer to override this method instead
        """
        pass

    def __init_subclass__(cls) -> None:
        """Called whenever a subclass inherits this class (i.e. at load time)"""

        # Store a reference to `cls` by date code 
        date_code = cls._infer_date_code()
        if date_code in SolutionBase._known_implementations:
            raise RuntimeError(f"Multiple implementations of {date_code}: {cls.__name__}")
        SolutionBase._known_implementations[date_code] = cls

    @classmethod
    def _infer_date_code(cls) -> DateCode:
        """
        Infer the date code based on the class name
        
        raise if the format is not recognized
        """

        n = cls.__name__
        m = _solution_name_re.match(n)
        if m:
            return DateCode(
                year=int(m[1]),
                day=int(m[2]),
            )
        
        raise RuntimeError(f"Cannot infer DateCode from: {n}")
    
    @classmethod
    def has_known_solution(cls, date_code: DateCode) -> bool:
        """Return `True` iff there is a known solution for `date_code`"""
        return date_code in SolutionBase._known_implementations

    @classmethod
    def run_known_solution(cls, date_code: DateCode) -> AnswerPair_T:
        """Run the known solution for a `date_code` with default parameters"""
        cls_to_run = SolutionBase._known_implementations[date_code]
        obj_to_run = cls_to_run()
        return obj_to_run.run()

    @property
    def part_1_answer(self) -> Optional[Answer_T]:
        """The answer for part 1"""
        if self._part_1_answer is None:
            self._part_1_answer = self._part_1_hook()
        return self._part_1_answer

    @property
    def part_2_answer(self) -> Optional[Answer_T]:
        """The answer for part 2"""
        if self._part_2_answer is None:
            self._part_2_answer = self._part_2_hook()
        return self._part_2_answer

    @property
    def raw_input(self) -> bytes:
        """return the raw input"""
        return self._input

    def is_part_1_done(self) -> bool:
        """Return `True` iff we have added an answer for part 1"""
        return self._part_1_answer is not None
    
    def is_part_2_done(self) -> bool:
        """Return `True` iff we have added an answer for part 2"""
        return self._part_2_answer is not None

    def input_str(self, encoding='ascii') -> str:
        """Return the input decoded into a string"""
        return self.raw_input.decode(encoding)

    def input_str_iter(
        self, 
        encoding='ascii',
        delim='\n',
        strip:bool = True
    ) -> list[str]:
        """Returns an iterator of the str, decoded, split, and possibly stripped"""
        l = self.input_str(encoding=encoding).split(delim)
        if strip:
            l = list(map(lambda x: x.strip(), l))
        return l

    def map_lines(
        self, 
        callable: Callable[[str], _MappedType_T], 
        include_empty_lines: bool = False,
        *args, **kwargs,
    ) -> Iterator[_MappedType_T]:
        """Map `callable` across the pieces of input determined by `input_str_iter`
        
        `args` and `kwargs` are passed down to `input_str_iter`

        By default, this is the lines of the input, with leading/trailing whitespace stripped
        """
        if include_empty_lines:
            return map(callable, self.input_str_iter(*args, **kwargs))
        else:
            return map(
                callable,
                filter(
                    lambda s: s,
                    self.input_str_iter(*args, **kwargs)
                )
            )

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Hook for implementing part 1"""
        return self.part_1_answer
    
    def _part_2_hook(self) -> Optional[Answer_T]:
        """Hook for implementing part 2"""
        return self.part_2_answer

    def run(self) -> AnswerPair_T:
        """Run part 1 then part 2 then report the answers"""
        return (self.part_1_answer, self.part_2_answer)
