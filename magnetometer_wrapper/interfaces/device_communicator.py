from traceback import StackSummary
from typing import Type, Iterator
import abc
from collections.abc import Iterable


class DeviceCommunicator(Iterable, metaclass=abc.ABCMeta):
    """
    Describes the interface for working with serial communication
    """
    @property
    @abc.abstractmethod
    def port(self) -> str:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def termination_characters(self) -> str:
        """

        :return: The termination characters of the message. The serial
        communicator will stop reading after this point
        """
        raise NotImplementedError()

    @termination_characters.setter
    def termination_characters(self, new_characters: str) -> None:
        """

        :param new_characters: The new termination characters
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def open(self) -> None:
        """
        Open the serial port
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def is_open(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def read(self) -> str:
        """

        :return: A single character read from the device.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def write(self, message: str) -> None:
        """

        :param message: The message to write without termination characters
        """
        raise NotImplementedError()

    def query(self, message: str) -> str:
        with self:
            self.write(message)
            result = self.read()
        return result

    @abc.abstractmethod
    def close(self) -> None:
        """
        Close the serial port
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def __enter__(self) -> 'DeviceCommunicator':
        """

        Open the serial port
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def __exit__(
            self,
            exc_type: Type[BaseException],
            exc_val: BaseException,
            exc_tb: StackSummary
    ) -> None:
        """

        Clean up the entire port

        :param exc_type: The type exception that was thrown
        :param exc_val: The
        :param exc_tb:
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def __iter__(self) -> Iterator[str]:
        """

        :return: A generator that returns the next character in the stream
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def __str__(self) -> str:
        """
        Read data coming in up to the termination characters
        """
        raise NotImplementedError()
