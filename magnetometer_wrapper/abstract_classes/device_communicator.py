"""
Contains an incomplete implementation of a ``DeviceCommunicator`` that seeks
to reduce the number of abstract methods that need to be implemented, at the
expense of providing some implementation of itself. Unlike the interfaces
defined in the ``interfaces`` module, it is not clear whether
``AbstractDeviceCommunicator`` will produce any issues when participating in
multiple inheritance.
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
    Provides an incomplete implementation for I/O with a device that uses a
    stateful port for communication.

    Subclasses of this need to implement a method to open and close the port,
    inspect the port's state, and read and write to the port. This class should
    be able to handle the rest of the state management.
    """
    def __init__(self, port: str, termination_characters='\r\n'):
        """

        :param port: The port to use for device I/O.
        :param termination_characters: The characters used to mark the end
            of a message. By default, these are ``\\r\\n``. The termination
            characters should match those set on the device with which I/O
            is to be established.
        """
        self._port = port
        self._terminator = termination_characters

    @abc.abstractmethod
    def open(self) -> None:
        """
        Open the port
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def is_open(self) -> bool:
        """

        :return: ``True`` if the port is open, otherwise ``False``
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def close(self) -> None:
        """
        Close the port
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def read(self) -> str:
        """

        :return: A single character read from the device
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def write(self, message: str) -> None:
        """

        :param message: The command to write to the device
        """
        raise NotImplementedError()

    @property
    def port(self) -> str:
        """

        :return: The port at which I/O has been established
        """
        return self._port

    @property
    def termination_characters(self) -> str:
        """

        :return: The characters used to mark the end of a message
        """
        return self._terminator

    @termination_characters.setter
    def termination_characters(self, new_terminator: str) -> None:
        """

        :param new_terminator: The new termination characters
        """
        self._terminator = new_terminator

    def query(self, message: str) -> str:
        """

        :param message: The message to send to the device
        :return: The output from the device, read up to the termination
            characters
        """
        with self:
            self.write(message)
            return self._last_read_message_from_device

    def __enter__(self) -> None:
        """
        Using the abstract ``open`` method, the entry into a context manager
        is managed by this method. This method opens the port.
        """
        if not self.is_open:
            log.debug('Opening port %s', self)
            self.open()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        This method is responsible for closing the port after exiting from
        the context manager.

        :param exc_type: The type exception that was thrown. ``None`` if no
            exception was thrown
        :param exc_val: The instance of the exception that was thrown.
            ``None`` if no exception was thrown
        :param exc_tb: The stack trace of the exception that was thrown.
            ``None`` if no exception was thrown
        """
        if self.is_open:
            log.debug('Closing port %s', self)
            self.close()

    def __iter__(self) -> Iterator[str]:
        """

        :return: An iterator that can be used to repeatedly call the
            ``read`` method. This is the primary way in which strings are
            read out from the device. This iterator will not return the
            termination characters
        """
        lookahead_buffer = self._get_lookahead_buffer()

        while self._should_keep_reading(lookahead_buffer):
            last_read_character = lookahead_buffer.popleft()
            lookahead_buffer.append(self.read())
            yield last_read_character

    @property
    def _last_read_message_from_device(self) -> Optional[str]:
        """

        :return: The last read message from the device, up to the
            termination character
        """
        result_string = ''.join(iter(self))
        log.info('Read message %s from port %s', result_string, self)
        return result_string

    def _should_keep_reading(self, lookahead_buffer: deque) -> bool:
        """

        :param lookahead_buffer: A queue containing the last few
            characters read by the iterator. This queue is as long as the
            string of termination characters. The contents of this queue are
            compared against the termination characters. If they match,
            the message is over and reading should stop
        :return: ``True` if reading should stop, otherwise ``False``.
        """
        return tuple(lookahead_buffer) != tuple(
            self.termination_characters
        )

    def _get_lookahead_buffer(self) -> deque:
        buffer = deque(maxlen=len(self.termination_characters))
        for _ in range(len(self.termination_characters)):
            buffer.append(self.read())
        return buffer

    def __repr__(self) -> str:
        """

        :return: The function call used to create this object
        """
        return '%s(port=%s, termination_characters=%s)' % (
            self.__class__.__name__, self.port, self.termination_characters
        )
