import re
from abc import ABC, abstractmethod


class Document(ABC):
    def __init__(self, value, validate=True):
        raw = self._clean(str(value)).zfill(self.length)
        self.raw = raw

        if validate and not self._is_valid():
            raise ValueError(f"Invalid {self.__class__.__name__}: {value}")

    def _clean(self, value: str) -> str:
        return re.sub(r"\D", "", value)

    @property
    @abstractmethod
    def length(self) -> int: ...

    @property
    @abstractmethod
    def formatted(self) -> str: ...

    @abstractmethod
    def _is_valid(self) -> bool: ...

    def is_valid(self) -> bool:
        return self._is_valid()

    @property
    def numbered(self) -> str:
        return self.raw

    def __eq__(self, other):
        if isinstance(other, Document):
            return self.raw == other.raw
        elif isinstance(other, str):
            return self.raw == self._clean(other).zfill(self.length)
        elif isinstance(other, int):
            return self.raw == str(other).zfill(self.length)
        return NotImplemented

    def __hash__(self):
        return hash(self.raw)

    def __str__(self):
        return self.formatted

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.formatted}')"
