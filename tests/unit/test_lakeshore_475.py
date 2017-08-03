"""
Contains unit tests for :mod:`magnetometer_wrapper.lakeshore_475`
"""
import unittest
import unittest.mock as mock
from math import inf, nan
from hypothesis import given
from hypothesis.strategies import floats, text
from magnetometer_wrapper.interfaces import DeviceCommunicator
from magnetometer_wrapper.lakeshore_475 import LakeShore475


class TestLakeshore475(unittest.TestCase):
    """
    Base class for the unit test
    """
    def setUp(self) -> None:
        """
        Create a mock wrapper for serial communication, and an
        implementation of the Lakeshore 475 that uses that wrapper
        """
        self.communicator = mock.MagicMock(spec=DeviceCommunicator)
        self.instrument = LakeShore475(self.communicator)


class TestField(TestLakeshore475):
    """
    Contains unit tests for the ``field`` method in the Lakeshore 475
    """
    @given(floats(allow_nan=False, allow_infinity=False))
    def test_field(self, expected_field: float) -> None:
        """
        Test that the magnetic field is correctly returned from the query
        method of the communicator

        :param float expected_field: The fake magnetic field measurement to
            return
        """
        self.communicator.query = mock.MagicMock(return_value=expected_field)
        self.assertAlmostEqual(expected_field, self.instrument.field)
        self.assertEqual(
            mock.call('RDGFIELD?'), self.communicator.query.call_args
        )

    def test_field_infinity(self) -> None:
        """
        Tests that if the measured magnetic field is infinity, that the
        units getter throws an ``IOError``
        """
        self.communicator.query = mock.MagicMock(return_value=inf)
        with self.assertRaises(IOError):
            _ = self.instrument.field

    def test_field_nan(self) -> None:
        """
        Tests that if the measured magnetic field is NaN, that the unit
        getter throws an ``IOError``
        """
        self.communicator.query = mock.MagicMock(return_value=nan)
        with self.assertRaises(IOError):
            _ = self.instrument.field


class TestUnitsSetter(TestLakeshore475):
    """
    Contains unit tests for the setter of ``units``
    """
    @given(text())
    def test_setter(self, new_units: str) -> None:
        self.instrument.units = new_units
        self.assertEqual(
            mock.call('UNITS %s' % new_units),
            self.communicator.query.call_args
        )


class TestRepr(TestLakeshore475):
    """
    Contains unit tests for the ``__repr__`` method of the Lakeshore 475
    """
    def test_repr(self):
        self.assertEqual(
            '%s(communicator=%s)' % (
                self.instrument.__class__.__name__, self.communicator
            ),
            self.instrument.__repr__()
        )
