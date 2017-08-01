"""

"""
import abc
from ..interfaces import DeviceCommunicator
from typing import Iterator, Optional
from collections import deque
import re
import logging

log = logging.getLogger(__name__)


class AbstractDeviceCommunicator(
    DeviceCommunicator, metaclass=abc.ABCMeta
):
    """

    """
    def __init__(self, port: str, termination_characters='\r\n'):
        self._port = port
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

    @abc.abstractmethod
    def read(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def write(self, message: str) -> None:
        raise NotImplementedError()

    @property
    def port(self) -> str:
        return self._port

    @property
    def termination_characters(self) -> str:
        return self._terminator

    @termination_characters.setter
    def termination_characters(self, new_terminator: str) -> None:
        self._terminator = new_terminator

    def query(self, message: str) -> str:
        with self:
            self.write(message)
            return self._last_read_message_from_device

    def __enter__(self) -> None:
        if not self.is_open:
            log.debug('Opening port %s', self)
            self.open()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.is_open:
            log.debug('Closing port %s', self)
            self.close()

    def __iter__(self) -> Iterator[str]:
        last_characters_read = deque(maxlen=len(self.termination_characters))
        while self._should_keep_reading(last_characters_read):
            new_char = self.read()
            last_characters_read.append(new_char)
            yield new_char

    @property
    def _last_read_message_from_device(self) -> Optional[str]:
        result_string = ''.join(iter(self))
        log.info('Read message %s from port %s', result_string, self)
        result = self._everything_but_terminator_regex.match(
            result_string
        )
        if result:
            return result.group(0)
        elif not result and result is not None:
            raise IOError('Unable to find termination characters in result')
        else:
            raise IOError('Unable to find a match for the termination '
                          'character regular expression. The result returned'
                          'None')

    def _should_keep_reading(self, last_characters_read: deque) -> bool:
        return tuple(last_characters_read) != tuple(
            self.termination_characters
        )

    @property
    def _everything_but_terminator_regex(self):
        return re.compile(r'^(.|\n)*(?={0}$)'.format(
            self.termination_characters)
        )

    def __repr__(self) -> str:
        return '%s(port=%s, termination_characters=%s)' % (
            self.__class__.__name__, self.port, self.termination_characters
        )
