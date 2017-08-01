import unittest
import unittest.mock as mock
from magnetometer_wrapper.abstract_classes import AbstractDeviceCommunicator
from hypothesis import given
from hypothesis.strategies import text


class TestAbstractDeviceCommunicator(unittest.TestCase):
    """
    Base class for the test
    """
    def setUp(self):
        self.communicator = self.ConcreteDeviceCommunicator()

    class ConcreteDeviceCommunicator(AbstractDeviceCommunicator):
        def __init__(self, port='foo', terminator=mock.MagicMock(spec=str)):
            super(
                TestAbstractDeviceCommunicator.ConcreteDeviceCommunicator,
                self
            ).__init__(port, termination_characters=terminator)
            self._is_open = False
            self.data_to_read = 'Foo'
            self.buffer = None
            self.mock_port = mock.MagicMock()
            self._last_read_index = 0

        def open(self):
            self._is_open = True
            self.mock_port.open()
            self._last_read_index = 0

        @property
        def is_open(self):
            return self._is_open

        @is_open.setter
        def is_open(self, is_open: bool) -> None:
            self._is_open = is_open

        def close(self):
            self._is_open = False
            self.mock_port.close()

        def read(self) -> str:
            character = self.data_to_read[self._last_read_index]
            self._last_read_index += 1
            return character

        def write(self, message: str) -> None:
            self.buffer = message

        def reset(self):
            self._port.reset_mock()
            self._is_open = False
            self._last_read_index = 0


class TestPort(TestAbstractDeviceCommunicator):
    @given(text())
    def test_port(self, port: str):
        comm = self.ConcreteDeviceCommunicator(port=port)
        self.assertEqual(comm.port, port)


class TestTerminationCharacterGetterAndSetter(TestAbstractDeviceCommunicator):
    @given(text())
    def test_getter_and_setter_for_terminator(self, terminator):
        self.communicator.termination_characters = terminator
        self.assertEqual(terminator, self.communicator.termination_characters)


class TestQuery(TestAbstractDeviceCommunicator):
    def setUp(self):
        TestAbstractDeviceCommunicator.setUp(self)
        self.terminator = '\r\n'
        self.communicator.termination_characters = self.terminator
        self.bad_message = 'bad message'

    @given(text(), text())
    def test_query_good_write(
            self, message_to_write: str, message_to_read: str
    ) -> None:
        self.communicator.data_to_read = message_to_read + self.terminator
        result = self.communicator.query(message_to_write)
        self.assertEqual(message_to_write, self.communicator.buffer)
        self.assertEqual(message_to_read, result)

    def test_query_bad_write(self):
        self.communicator.write = mock.MagicMock(side_effect=ValueError())
        with self.assertRaises(ValueError):
            _ = self.communicator.query(self.bad_message)

        self.assertTrue(self.communicator.mock_port.close.called)


class TestEnter(TestAbstractDeviceCommunicator):
    def test_enter_unopened_port(self):
        with self.communicator:
            self.assertTrue(self.communicator.mock_port.open.called)
            self.assertFalse(self.communicator.mock_port.close.called)

    def test_enter_open_port(self):
        self.communicator.is_open = True
        with self.communicator:
            self.assertFalse(self.communicator.mock_port.open.called)
            self.assertFalse(self.communicator.mock_port.close.called)


class TestExit(TestAbstractDeviceCommunicator):
    def test_exit_open_port(self):
        with self.communicator:
            self.assertTrue(self.communicator.mock_port.open.called)
            self.assertFalse(self.communicator.mock_port.close.called)
        self.assertTrue(self.communicator.mock_port.close.called)

    def test_exit_closed_port(self):
        with self.communicator:
            self.assertTrue(self.communicator.mock_port.open.called)
            self.communicator.is_open = False
        self.assertFalse(self.communicator.mock_port.close.called)