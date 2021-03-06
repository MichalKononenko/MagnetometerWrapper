"""
Describes how to work with RS232 ports. This interface extends the
``DeviceCommunicator`` to work with devices working over an RS232 port.
"""
from enum import Enum, unique
import abc
from .device_communicator import DeviceCommunicator


class SerialCommunicator(DeviceCommunicator, metaclass=abc.ABCMeta):
    """
    Provides I/O between devices over an RS232 serial port. This is
    accomplished by using pySerial as a networking layer. In order to do
    this, some additional parameters need to be specified when working with
    RS232 ports.

    *Characters*
    RS232 streams data in terms of characters, which consist of a start bit, a
    number of data bits, a number of parity bits, and a number of stop bits.
    """

    @unique
    class Databits(Enum):
        """
        The possible values for the data bits in the serial stream. The
        number of data bits represents the number of bits that are used to
        encode a character in a particular character sent in an RS232 stream.

        In the case of the Lakeshore 475 gaussmeter, the device communicates
        using seven data bits. This means that the data_bits parameter should
        be set to ``SEVEN``.
        """
        EIGHT = "EIGHT"
        SEVEN = "SEVEN"
        SIX = "SIX"
        FIVE = "FIVE"

    @unique
    class StopBits(Enum):
        """
        The possible stop bits, to be used for marking the end of an RS232
        character.
        """
        ONE = "ONE"
        ONE_POINT_FIVE = "ONE_POINT_FIVE"
        TWO = "TWO"

    @unique
    class ParityBits(Enum):
        """
        The parity scheme to use for error detection in the RS232 scheme. An
        ``ODD`` parity is one where the parity bit is flipped in order to
        ensure that the total number of bits in the character is odd. An
        ``EVEN`` parity will flip the error detection bit in order to keep
        the number of bits in a character even. The use of the parity bit
        protects against single bit-flip errors in transmission.
        """
        ODD = "ODD"
        EVEN = "EVEN"

    @property
    @abc.abstractmethod
    def parity_bits(self) -> ParityBits:
        """

        :return: The current parity bit scheme being used by the communicator
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def stop_bits(self) -> StopBits:
        """

        :return: The current number of stop bits being used by the
            communicator
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def data_bits(self) -> Databits:
        """

        :return: The number of data bits currently being used
        """
        raise NotImplementedError()

    @property
    def baud_rate(self) -> int:
        """

        :return: The baud rate (digital signal frequency) in bits per second

        """
        raise NotImplementedError()

    @baud_rate.setter
    def baud_rate(self, new_baud: int) -> None:
        """

        :param new_baud: The desired baud rate
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def read_timeout(self) -> float:
        """

        :return: The time that will have to elapse before the reading of a
            character times out
        """
        raise NotImplementedError()

    @read_timeout.setter
    @abc.abstractmethod
    def read_timeout(self, new_timeout: int) -> None:
        """

        :param new_timeout: The desired timeout

        """
        raise NotImplementedError()
