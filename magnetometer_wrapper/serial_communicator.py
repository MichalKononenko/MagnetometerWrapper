from .abstract_classes import AbstractDeviceCommunicator
from .interfaces import SerialCommunicator as SerialCommunicatorInterface
import serial


class SerialCommunicator(
    AbstractDeviceCommunicator, SerialCommunicatorInterface
):
    """
    Base class for serial communication
    """

    _DATA_BIT_CONVERTER = {
        SerialCommunicatorInterface.Databits.FIVE:
            serial.FIVEBITS,
        SerialCommunicatorInterface.Databits.SIX:
            serial.SIXBITS,
        SerialCommunicatorInterface.Databits.SEVEN:
            serial.SEVENBITS,
        SerialCommunicatorInterface.Databits.EIGHT:
            serial.EIGHTBITS
    }

    _STOP_BIT_CONVERTER = {
        SerialCommunicatorInterface.StopBits.ONE:
            serial.STOPBITS_ONE,
        SerialCommunicatorInterface.StopBits.ONE_POINT_FIVE:
            serial.STOPBITS_ONE_POINT_FIVE,
        SerialCommunicatorInterface.StopBits.TWO:
            serial.STOPBITS_TWO
    }

    _PARITY_BIT_CONVERTER = {
        SerialCommunicatorInterface.ParityBits.ODD:
            serial.PARITY_ODD
    }

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
            termination_characters: str='\r\n'
    ) -> None:
        super(SerialCommunicator, self).__init__(port, termination_characters)
        self._serial = serial.Serial(
            port=port,
            baudrate=baud_rate,
            data_bits=self._DATA_BIT_CONVERTER[data_bits],
            stop_bits=self._STOP_BIT_CONVERTER[stop_bits],
            parity=self._PARITY_BIT_CONVERTER[parity_bits]
        )

    def open(self):
        self._serial.open()

    @property
    def is_open(self) -> bool:
        return self._serial.is_open

    def close(self):
        self._serial.close()

    def read(self) -> str:
        return self._serial.read()

    def write(self, message: str) -> None:
        self._serial.write(self._get_data_to_write(message))

    @property
    def parity_bits(self) -> SerialCommunicatorInterface.ParityBits:
        parity = self._serial.parity

        if parity == serial.PARITY_ODD:
            return SerialCommunicatorInterface.ParityBits.ODD
        else:
            raise AttributeError('Unable to convert parity bits to the enum')

    @property
    def stop_bits(self) -> SerialCommunicatorInterface.StopBits:
        stop_bits = self._serial.stopbits

        if stop_bits == serial.STOPBITS_ONE:
            return SerialCommunicatorInterface.StopBits.ONE
        elif stop_bits == serial.STOPBITS_ONE_POINT_FIVE:
            return SerialCommunicatorInterface.StopBits.ONE_POINT_FIVE
        elif stop_bits == serial.STOPBITS_TWO:
            return SerialCommunicatorInterface.StopBits.TWO
        else:
            raise AttributeError(
                'Unable to convert stop bits to the required enum'
            )

    @property
    def data_bits(self) -> SerialCommunicatorInterface.Databits:
        data_bits = self._serial.bytesize

        if data_bits == serial.FIVEBITS:
            return SerialCommunicatorInterface.Databits.FIVE
        elif data_bits == serial.SIXBITS:
            return SerialCommunicatorInterface.Databits.SIX
        elif data_bits == serial.SEVENBITS:
            return SerialCommunicatorInterface.Databits.SEVEN
        elif data_bits == serial.EIGHTBITS:
            return SerialCommunicatorInterface.Databits.EIGHT
        else:
            raise AttributeError(
                'Unable to convert data bits to the required enum'
            )

    @property
    def baud_rate(self) -> int:
        return self._serial.baudrate

    @baud_rate.setter
    def baud_rate(self, new_baud: int) -> None:
        self._serial.baudrate = new_baud

    def _get_data_to_write(self, message: str) -> bytes:
        string_data = message + self.termination_characters
        return string_data.encode('utf-8')
