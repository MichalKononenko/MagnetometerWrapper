import abc


class Magnetometer(object, metaclass=abc.ABCMeta):
    """
    Describes the type and contract for the magnetometer
    """
    @property
    @abc.abstractmethod
    def field(self) -> float:
        """

        :return: The current magnetic field
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def units(self):
        """

        :return: The units that are being used to measure the magnetic field
        """
        raise NotImplementedError()

    @units.setter
    def units(self, new_unit) -> None:
        """

        :param new_unit: The new unit to use to measure the magnetic field
        """
        raise NotImplementedError()
