"""
Contains an interface that describes how to perform device I/O.
"""
from typing import Type, Iterator, Optional, Any
import abc
from collections.abc import Iterable


class DeviceCommunicator(Iterable, metaclass=abc.ABCMeta):
    """
    Describes the interface for working with serial communication
    """
    @property
    @abc.abstractmethod
    def port(self) -> str:
        """

        :return: A string representation of the port to which this
        communicator is bound. For instance, if this communicator is bound
        to a serial port, the port could be set to something like
        ``/dev/ttyUSB0`` on Linux, or ``COM1`` on Windows.
        """
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
        """

        :return: ``True`` if the port is open and ``False`` if not
        """
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

    @abc.abstractmethod
    def query(self, message: str) -> str:
        """
        Send a command to the device and wait for a response

        :param message: The command to be sent to the device, without
            termination characters
        :return: The response from the device
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def close(self) -> None:
        """
        Close the serial port
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def __enter__(self) -> 'DeviceCommunicator':
        """

        Prepare the communicator for communicating with the device
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[Any]
    ) -> None:
        """

        Clean the communicator up after communication has completed.

        :param exc_type: The type exception that was thrown. ``None`` if no
            exception was thrown
        :param exc_val: The instance of the exception that was thrown.
        ``None`` if no exception was thrown
        :param exc_tb: The stack trace of the exception that was thrown.
        ``None`` if no exception was thrown
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def __iter__(self) -> Iterator[str]:
        """

        .. note::

            The communicator is not responsible for reading a particular
            number of characters out of the device. If the device reads out
            an infinite number of characters, then this iterator will not
            exit. In order to read a finite number of characters, consider
            wrapping this generator in ``itertools.islice``.

        :return: A generator that returns the characters in the stream. This
        should repeatedly call ``read`` until the termination characters are
        hit. This method is responsible for determining when to stop iteration.
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def _last_read_message_from_device(self) -> str:
        """
        Read data coming in up to the termination characters, returning the
        message as a string

        :return The string read from the device, minus any termination
            characters
        """
        raise NotImplementedError()
