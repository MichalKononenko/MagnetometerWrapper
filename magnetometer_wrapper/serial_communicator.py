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
        super(SerialCommunicator, self).__init__(port, termination_characters)
        self._serial = serial_constructor(
            port=port,
            baudrate=baud_rate,
            bytesize=data_bits.value,
            stopbits=stop_bits.value,
            parity=parity_bits.value,
            timeout=timeout
        )

    def open(self):
        log.info('Opening serial port %s', self._serial)
        self._serial.open()

    @property
    def is_open(self) -> bool:
        return self._serial.isOpen()

    def close(self):
        log.info('Closing serial port %s', self._serial)
        self._serial.close()

    def read(self) -> str:
        character = self._serial.read().decode('utf-8', errors='strict')
        log.debug('Read character %s from port %s', character, self._serial)
        return character

    def write(self, message: str) -> None:
        log.info('Wrote message %s to port %s', message, self._serial)
        self._serial.write(self._get_data_to_write(message))

    @property
    def parity_bits(self) -> SerialCommunicatorInterface.ParityBits:
        return SerialCommunicator.ParityBits(self._serial.parity)

    @property
    def stop_bits(self) -> SerialCommunicatorInterface.StopBits:
        return SerialCommunicator.StopBits(self._serial.stopbits)

    @property
    def data_bits(self) -> SerialCommunicatorInterface.Databits:
        return SerialCommunicator.Databits(self._serial.bytesize)

    @property
    def baud_rate(self) -> int:
        return self._serial.baudrate

    @baud_rate.setter
    def baud_rate(self, new_baud: int) -> None:
        self._serial.baudrate = new_baud

    def _get_data_to_write(self, message: str) -> bytes:
        string_data = message + self.termination_characters
        return string_data.encode('utf-8')

    @property
    def read_timeout(self) -> int:
        return self._serial.timeout

    @read_timeout.setter
    def read_timeout(self, new_timeout: int) -> None:
        self._serial.timeout = new_timeout
