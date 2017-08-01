import serial
from enum import Enum
import abc
from .device_communicator import DeviceCommunicator


class SerialCommunicator(DeviceCommunicator, metaclass=abc.ABCMeta):
    class Databits(Enum):
        EIGHT = serial.EIGHTBITS
        SEVEN = serial.SEVENBITS
        SIX = serial.SIXBITS
        FIVE = serial.FIVEBITS

    class StopBits(Enum):
        ONE = serial.STOPBITS_ONE
        ONE_POINT_FIVE = serial.STOPBITS_ONE_POINT_FIVE
        TWO = serial.STOPBITS_TWO

    class ParityBits(Enum):
        ODD = serial.PARITY_ODD

    @property
    @abc.abstractmethod
    def parity_bits(self) -> ParityBits:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def stop_bits(self) -> StopBits:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def data_bits(self) -> Databits:
        raise NotImplementedError()

    @property
    def baud_rate(self) -> int:
        raise NotImplementedError()

    @baud_rate.setter
    def baud_rate(self, new_baud: int) -> None:
        raise NotImplementedError()
