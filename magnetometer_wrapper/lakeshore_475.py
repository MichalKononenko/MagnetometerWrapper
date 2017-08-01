from .interfaces import Magnetometer, DeviceCommunicator


class LakeShore475(Magnetometer):
    def __init__(self, communicator: DeviceCommunicator):
        self._comm = communicator

    @property
    def field(self):
        field_response = self._comm.query('RDGFIELD?')
        return float(field_response)

    @property
    def units(self):
        return float(self._comm.query('UNITS?'))

    @units.setter
    def units(self, new_unit: str) -> None:
        self._comm.query('UNITS {0}'.format(new_unit))
