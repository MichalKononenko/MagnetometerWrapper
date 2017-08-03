"""
Contains unit tests for
:mod:`magnetometer_wrapper.serial_communicator`
"""
import unittest
import unittest.mock as mock
from serial import Serial
from magnetometer_wrapper.serial_communicator import SerialCommunicator
from hypothesis import given
from hypothesis.strategies import text, sampled_from, integers, characters


class TestSerialCommunicator(unittest.TestCase):
    """
    Base class for unit-testing of the module
    """
    def setUp(self) -> None:
        """
        Set up the environment for the test
        """
        self.port = '/dev/ttyUSB0'
        self.serial_port = mock.MagicMock(spec=Serial)
        self.serial_constructor = mock.MagicMock(
            spec=Serial.__class__, return_value=self.serial_port
        )
        self.serial = SerialCommunicator(
            self.port, serial_constructor=self.serial_constructor
        )


class TestOpen(TestSerialCommunicator):
    """
    Contains unit tests for the ``open`` method in the serial communicator
    """
    def test_open(self) -> None:
        """
        Checks that the mock serial library's ``open`` method is called when
        the
        """
        self.serial.open()
        self.assertTrue(self.serial_constructor().open.called)


class TestIsOpen(TestSerialCommunicator):
    """
    Contains unit tests for the ``is_open`` method
    """
    def test_is_open(self) -> None:
        """
        Checks that the serial library's ``isOpen`` method is used to check
        whether the port is open or not
        """
        self.assertEqual(
            self.serial.is_open,
            self.serial_port.isOpen()
        )


class TestRead(TestSerialCommunicator):
    """
    Contains unit tests for the ``read`` method
    """
    def test_read(self) -> None:
        """
        Checks that the ``read`` method returns a single character obtained
        via the serial library's ``read`` method
        """
        self.assertEqual(
            self.serial.read(),
            self.serial_port.read().decode('utf-8')
        )

    @given(characters())
    def test_read_binary_input(self, character: str) -> None:
        """

        :param character: A randomly-generated character to be read from the
            device
        """
        self.serial_port.read = mock.MagicMock(
            return_value=character.encode('utf-8')
        )
        self.assertEqual(self.serial.read(), character)


class TestWrite(TestSerialCommunicator):
    """
    Contains unit tests for the ``write`` method of the serial communicator
    """
    @given(text())
    def test_write(self, message: str) -> None:
        """
        Contains unit tests for the serial communicator's ``write`` method

        :param message: A randomly-generated message to write
        """
        self.serial.write(message)

        expected_bytes_written = (
            message + self.serial.termination_characters
        ).encode('utf-8')

        self.assertEqual(
            mock.call(expected_bytes_written),
            self.serial_port.write.call_args
        )


class TestParityBits(TestSerialCommunicator):
    """
    Contains unit tests for the getter and setter of the ``ParityBits``
    parameter
    """
    @given(sampled_from(SerialCommunicator.ParityBits))
    def test_parity_bits(self, parity: SerialCommunicator.ParityBits) -> None:
        """

        :param parity: The desired parity to set, and check for matching parity
        """
        self.serial_port.parity = parity.value
        comm = SerialCommunicator(
            self.port, parity_bits=parity,
            serial_constructor=self.serial_constructor
        )
        self.assertIs(comm.parity_bits, parity)


class TestStopBits(TestSerialCommunicator):
    """
    Contains unit tests for the getter and setter parameters for the stop
    bits parameter
    """
    @given(sampled_from(SerialCommunicator.StopBits))
    def test_stop_bits(self, stop_bits: SerialCommunicator.StopBits) -> None:
        """
        Tests that the stop bits are retrieved and set correctly

        :param stop_bits: A randomly-generated stop bit parameter to set
        """
        self.serial_port.stopbits = stop_bits.value
        comm = SerialCommunicator(
            self.port, stop_bits=stop_bits,
            serial_constructor=self.serial_constructor
        )
        self.assertIs(comm.stop_bits, stop_bits)


class TestDataBits(TestSerialCommunicator):
    """
    Contains unit tests for the ``data_bits`` parameter in the serial
    connection
    """
    @given(sampled_from(SerialCommunicator.Databits))
    def test_data_bits(self, data_bits: SerialCommunicator.Databits) -> None:
        """
        Test that the data bits are set and retrieved correctly

        :param data_bits: The desired data bits to set
        """
        self.serial_port.bytesize = data_bits.value
        comm = SerialCommunicator(
            self.port, data_bits=data_bits,
            serial_constructor=self.serial_constructor
        )
        self.assertIs(comm.data_bits, data_bits)


class TestBaudRate(TestSerialCommunicator):
    """
    Contains unit tests for the getter and setter for the baud rate parameter
    """
    @given(integers())
    def test_baud_rate(self, new_baud: int) -> None:
        """

        :param new_baud: A randomly-generated baud rate to set
        """
        self.serial.baud_rate = new_baud
        self.assertEqual(self.serial.baud_rate, new_baud)
        self.assertEqual(self.serial_port.baudrate, new_baud)
