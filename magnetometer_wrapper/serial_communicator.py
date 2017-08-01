"""
Contains an implementation of ``SerialCommunicator``. Manages communication
over RS232.
"""
from .abstract_classes import AbstractDeviceCommunicator
from .interfaces import SerialCommunicator as SerialCommunicatorInterface
import serial
from typing import Type
import logging

log = logging.getLogger(__name__)


class SerialCommunicator(
    AbstractDeviceCommunicator, SerialCommunicatorInterface
):
    """
    Base class for serial communication
    """
    def __init__(
            self,
            port: str,
            baud_rate: int=9600,
            data_bits: SerialCommunicatorInterface.Databits=
            SerialCommunicatorInterface.Databits.SEVEN,
            stop_bits: SerialCommunicatorInterface.StopBits=
            SerialCommunicatorInterface.StopBits.ONE,
            parity_bits: SerialCommunicatorInterface.ParityBits=
            SerialCommunicatorInterface.ParityBits.ODD,
            termination_characters: str='\r\n',
            serial_constructor: Type[serial.Serial]=serial.Serial,
            timeout: float=3
    ) -> None:
        """

        :param port: The port for which communication is to be established
        :param baud_rate: The data transfer rate in bits per second
        :param data_bits: The number of data bits
        :param stop_bits: The number of stop bits
        :param parity_bits: The parity scheme
        :param termination_characters: The string of characters used to mark
            the end of communication
        :param serial_constructor: The class to use for making the serial
            hardware. This is often altered for testing, in order to allow
            pySerial to be stubbed out
        :param timeout: The amount of time to elapse before the communicator
            gives up on reading a character
        """
        super(SerialCommunicator, self).__init__(port, termination_characters)
        self._serial = serial_constructor(
            port=port,
            baudrate=baud_rate,
            bytesize=data_bits.value,
            stopbits=stop_bits.value,
            parity=parity_bits.value,
            timeout=timeout
        )

    def open(self) -> None:
        """
        Open the serial port
        """
        log.info('Opening serial port %s', self._serial)
        self._serial.open()

    @property
    def is_open(self) -> bool:
        """

        :return: ``True`` if the port is open, otherwise ``False``
        """
        return self._serial.isOpen()

    def close(self):
        """
        Close the serial port
        """
        log.info('Closing serial port %s', self._serial)
        self._serial.close()

    def read(self) -> str:
        """

        :return: A single character read from the device
        """
        character = self._serial.read().decode('utf-8', errors='strict')
        log.debug('Read character %s from port %s', character, self._serial)
        return character

    def write(self, message: str) -> None:
        """

        Write a string to the device

        :param message: The message to write to the device, without
            termination characters
        """
        log.info('Wrote message %s to port %s', message, self._serial)
        self._serial.write(self._get_data_to_write(message))

    @property
    def parity_bits(self) -> SerialCommunicatorInterface.ParityBits:
        """

        :return: The parity bits
        """
        return SerialCommunicator.ParityBits(self._serial.parity)

    @property
    def stop_bits(self) -> SerialCommunicatorInterface.StopBits:
        """

        :return: The stop bits
        """
        return SerialCommunicator.StopBits(self._serial.stopbits)

    @property
    def data_bits(self) -> SerialCommunicatorInterface.Databits:
        """

        :return: The number of data bits
        """
        return SerialCommunicator.Databits(self._serial.bytesize)

    @property
    def baud_rate(self) -> int:
        """

        :return: The baud rate
        """
        return self._serial.baudrate

    @baud_rate.setter
    def baud_rate(self, new_baud: int) -> None:
        """

        :param new_baud: The desired baud rate
        """
        self._serial.baudrate = new_baud

    def _get_data_to_write(self, message: str) -> bytes:
        """
        Append the terminator characters to the message to send to the
        device, and convert it to a byte array
        :param str message: The message to write
        :return: The encoded message
        """
        string_data = message + self.termination_characters
        return string_data.encode('utf-8')

    @property
    def read_timeout(self) -> int:
        """

        :return: The read timeout
        """
        return self._serial.timeout

    @read_timeout.setter
    def read_timeout(self, new_timeout: int) -> None:
        """

        :param new_timeout: The desired timeout
        """
        self._serial.timeout = new_timeout
