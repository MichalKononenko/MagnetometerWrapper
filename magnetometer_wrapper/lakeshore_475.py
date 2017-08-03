"""
Contains an implementation of magnetometer interface for the
Lakeshore 475 gaussmeter. The queries here are related to working with this
specific model of gaussmeter.
"""
from .interfaces import Magnetometer, DeviceCommunicator
from math import isnan, isinf


class LakeShore475(Magnetometer):
    """
    Implements the magnetometer
    """
    def __init__(self, communicator: DeviceCommunicator):
        """

        :param communicator: The implementation of ``DeviceCommunicator``
            that will be used to perform I/O with the gaussmeter
        """
        self._communicator = communicator

    @property
    def field(self) -> float:
        """

        :return: The measured magnetic field
        :raises: :exc:`IOError` if, after conversion to a floating-point
            number, the magnetic field is either infinity or NaN
        """
        field_response = float(self._communicator.query('RDGFIELD?'))

        if isnan(field_response):
            raise IOError('The device returned a magnetic field of NaN')
        if isinf(field_response):
            raise IOError('The device returned an infinite magnetic field')

        return float(field_response)

    @property
    def units(self) -> str:
        """

        :return: The units being used to measure the magnetic field
        """
        return str(self._communicator.query('UNITS?'))

    @units.setter
    def units(self, new_unit: str) -> None:
        """

        :param new_unit: The new unit to be sets
        """
        self._communicator.query('UNITS {0}'.format(new_unit))

    def __repr__(self) -> str:
        """

        :return: The Python code used to create the instance
        """
        return '%s(communicator=%s)' % (
            self.__class__.__name__, self._communicator
        )
