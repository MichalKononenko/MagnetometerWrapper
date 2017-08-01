"""
Contains integration tests for the gaussmeter
"""
import unittest
from magnetometer_wrapper.lakeshore_475 import LakeShore475
from magnetometer_wrapper.serial_communicator import SerialCommunicator
import logging

logging.basicConfig(level=logging.DEBUG)


class TestLakeshore475(unittest.TestCase):
    def setUp(self):
        self.port = '/dev/ttyUSB0'
        self.data_bits = SerialCommunicator.Databits.SEVEN
        self.stop_bits = SerialCommunicator.StopBits.ONE
        self.parity_bits = SerialCommunicator.ParityBits.ODD
        self.terminator = '\r\n'

        self.communicator = SerialCommunicator(
            port=self.port, data_bits=self.data_bits,
            stop_bits=self.stop_bits, parity_bits=self.parity_bits,
            termination_characters=self.terminator
        )

        self.instrument = LakeShore475(self.communicator)


class TestCommunicator(TestLakeshore475):
    def setUp(self):
        TestLakeshore475.setUp(self)
        self.identity_query = '*IDN?'

    def test_communicator(self):
        result = self.communicator.query(self.identity_query)
        print(result)
        self.assertIsInstance(result, str)


class TestField(TestLakeshore475):
    def test_field(self):
        print(self.instrument.field)
        self.assertIsInstance(self.instrument.field, float)


class TestUnits(TestLakeshore475):
    def test_unit_gauss(self):
        self.instrument.units = 'G'
        self.assertEqual('G', self.instrument.units)

    def test_unit_amp(self):
        self.instrument.units = 'A'
        self.assertEqual('A', self.instrument.units)
