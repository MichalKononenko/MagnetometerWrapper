import abc
from ..interfaces import DeviceCommunicator
from typing import Iterator
from collections import deque


class AbstractDeviceCommunicator(
    DeviceCommunicator, metaclass=abc.ABCMeta
):
    """

    """
    def __init__(self, termination_characters='\r\n'):
        self._terminator = termination_characters

    @abc.abstractmethod
    def open(self) -> None:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def is_open(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def close(self) -> None:
        raise NotImplementedError()

    @property
    def termination_characters(self) -> str:
        return self._terminator

    @termination_characters.setter
    def termination_characters(self, new_terminator: str) -> None:
        self._terminator = new_terminator

    def __enter__(self) -> None:
        if not self.is_open:
            self.open()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.is_open:
            self.close()

    def __iter__(self) -> Iterator[str]:
        last_characters_read = deque(maxlen=len(self.termination_characters))
        with self:
            new_char = self.read()
            last_characters_read.append(new_char)
            if self._should_stop(last_characters_read):
                raise StopIteration()
            else:
                yield new_char

    def __str__(self) -> str:
        return ''.join(char for char in self)

    def _should_stop(self, last_characters_read: deque) -> bool:
        return tuple(last_characters_read) == tuple(self.termination_characters)