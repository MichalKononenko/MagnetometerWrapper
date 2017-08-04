"""
Contains unit tests for
:mod:`magnetometer_wrapper.abstract_classes.device_communicator`
"""
import unittest
import unittest.mock as mock
from magnetometer_wrapper.abstract_classes import AbstractDeviceCommunicator
from hypothesis import given
from hypothesis.strategies import text
import logging
import re

logging.basicConfig(level=logging.DEBUG)


class TestAbstractDeviceCommunicator(unittest.TestCase):
    """
    Base class for unit testing of the module
    """
    def setUp(self) -> None:
        """
        Create a communicator that is an instance of the abstract device
        communicator. This communicator has a minimal implementation of all
        the methods required by the ``AbstractDeviceCommunicator``
        """
        self.communicator = self.ConcreteDeviceCommunicator()

    def tearDown(self) -> None:
        """
        Reset the communicator
        """
        self.communicator.reset()

    class ConcreteDeviceCommunicator(AbstractDeviceCommunicator):
        """
        Since ``AbstractDeviceCommunicator`` cannot be instantiated
        directly, this class provides a small implementation of all the
        methods required to instantiate the ``AbstractDeviceCommunicator``.
        """
        def __init__(
                self,
                port: str=mock.MagicMock(spec=str),
                terminator: str=mock.MagicMock(spec=str)
        ):
            """

            :param port: A mock port with which I/O is to be established
            :param terminator: The termination characters
            """
            super(
                TestAbstractDeviceCommunicator.ConcreteDeviceCommunicator,
                self
            ).__init__(port, termination_characters=terminator)
            self._is_open = False
            self.data_to_read = 'Foo'
            self.buffer = None
            self.mock_port = mock.MagicMock()
            self._last_read_index = 0

        def open(self) -> None:
            """
            Indicate to the test fixture that the port has been opened
            """
            self._is_open = True
            self.mock_port.open()
            self._last_read_index = 0

        @property
        def is_open(self) -> bool:
            """

            :return: The fake state of the open "port"
            """
            return self._is_open

        @is_open.setter
        def is_open(self, is_open: bool) -> None:
            """
            Set the open state in order to test for things like the port
            closing unexpectedly

            :param is_open: The new state of the open "port"
            """
            self._is_open = is_open

        def close(self) -> None:
            """
            Close the fake port
            """
            self._is_open = False
            self.mock_port.close()

        def read(self) -> str:
            """

            :return: A single character read from the data to read
            """
            character = self.data_to_read[self._last_read_index]
            self._last_read_index += 1
            return character

        def write(self, message: str) -> None:
            """
            Take the argument, and write it to a buffer for later inspection
            during testing

            :param message: The string to write
            """
            self.buffer = message

        def reset(self) -> None:
            """
            After a test is complete, bring the fixture back to a known state
            """
            self._is_open = False
            self._last_read_index = 0


class TestPort(TestAbstractDeviceCommunicator):
    @given(text())
    def test_port(self, port: str) -> None:
        """
        Check that the port parameter is correctly set

        :param port: A randomly-generated port name
        """
        comm = self.ConcreteDeviceCommunicator(port=port)
        self.assertEqual(comm.port, port)


class TestTerminationCharacterGetterAndSetter(TestAbstractDeviceCommunicator):
    """
    Contains unit tests for the termination character setter and getter
    """
    @given(text())
    def test_getter_and_setter_for_terminator(self, terminator: str) -> None:
        """
        Tests that the termination character is correctly set to a new
        value, and that the getter returns the value of the termination
        character that was just obtained

        :param terminator: A randomly-generated string representing the
            termination characters
        """
        self.communicator.termination_characters = terminator
        self.assertEqual(terminator, self.communicator.termination_characters)


class TestQuery(TestAbstractDeviceCommunicator):
    """
    Contains unit tests for the ``query`` method in the abstract device
    communicator
    """
    def setUp(self) -> None:
        """
        Set the terminator to a realistic ``\\r\\n``, and prepare a dummy
        bad message to test what happens if the writing doesn't work
        correctly during the query
        """
        TestAbstractDeviceCommunicator.setUp(self)
        self.terminator = '\r\n'
        self.communicator.termination_characters = self.terminator
        self.bad_message = 'bad message'

    @given(text(), text())
    def test_query_good_write(
            self, message_to_write: str, message_to_read: str
    ) -> None:
        """
        Tests that the query method successfully writes data to the device,
        and reads the data returned from the device

        :param message_to_write: A randomly-generated string representing
            the message to be written to the mock device
        :param message_to_read: A randomly-generated string representing the
            response to be read from the mock device
        """
        data_to_read = message_to_read + self.terminator
        self.communicator.data_to_read = data_to_read
        result = self.communicator.query(message_to_write)
        self.assertEqual(message_to_write, self.communicator.buffer)
        self.assertEqual(message_to_read, result)

    def test_query_bad_write(self) -> None:
        """
        Tests that if the write method of the query fails, then the port is
        still successfully closed, and the exception that caused the write
        failure is thrown
        """
        self.communicator.write = mock.MagicMock(side_effect=Exception())
        with self.assertRaises(Exception):
            _ = self.communicator.query(self.bad_message)

        self.assertTrue(self.communicator.mock_port.close.called)

    def test_query_bad_read(self) -> None:
        """
        Tests that if the read method in the query fails, then the port is
        still successfully closed, and the exception that caused the read
        failure is thrown
        """
        self.communicator.read = mock.MagicMock(side_effect=Exception())
        with self.assertRaises(Exception):
            _ = self.communicator.query(self.bad_message)

        self.assertTrue(self.communicator.mock_port.close.called)


class TestEnter(TestAbstractDeviceCommunicator):
    """
    Contains unit tests for the ``__enter__`` method of the
    ``DeviceCommunicator``'s context manager
    """
    def test_enter_unopened_port(self) -> None:
        """
        Tests that the port is opened if the port started unopened
        """
        with self.communicator:
            self.assertTrue(self.communicator.mock_port.open.called)
            self.assertFalse(self.communicator.mock_port.close.called)

    def test_enter_open_port(self) -> None:
        """
        Tests that the port is not opened if the port started opened
        """
        self.communicator.is_open = True
        with self.communicator:
            self.assertFalse(self.communicator.mock_port.open.called)
            self.assertFalse(self.communicator.mock_port.close.called)


class TestExit(TestAbstractDeviceCommunicator):
    """
    Contains unit tests for the ``__exit__`` method of the
    ``DeviceCommunicator``'s context manager
    """
    def test_exit_open_port(self) -> None:
        """
        Tests that if the port is opened, that it is closed after the
        context manager exits
        """
        with self.communicator:
            self.assertTrue(self.communicator.mock_port.open.called)
            self.assertFalse(self.communicator.mock_port.close.called)
        self.assertTrue(self.communicator.mock_port.close.called)

    def test_exit_closed_port(self):
        """
        Tests that if the port is closed in the context manager, then no
        attempt is made to close the port again after leaving the context
        manager.
        """
        with self.communicator:
            self.assertTrue(self.communicator.mock_port.open.called)
            self.communicator.is_open = False
        self.assertFalse(self.communicator.mock_port.close.called)


class TestIter(TestAbstractDeviceCommunicator):
    """
    Contains unit tests for the ``__iter__`` generator, responsible for
    iteratively reading all the characters in the message
    """
    @given(text(), text(min_size=1))
    def test_iter(self, message: str, terminator: str) -> None:
        """
        Tests that the iterator returns a random message to be read,
        less any termination characters

        :param message: The message that the iterator should read, character
            by character
        """
        data_to_read = message + terminator
        self.communicator.termination_characters = terminator
        self.communicator.data_to_read = data_to_read

        with self.communicator:
            response = ''.join(char for char in self.communicator)

        self.assertEqual(
            self._get_expected_characters_that_were_read(
                message, terminator
            ), response
        )

    @staticmethod
    def _get_expected_characters_that_were_read(
            message: str, terminator: str
    ) -> str:
        """

        Given a randomly-generated message and terminator from hypothesis,
        get only the first characters in the message that come from the
        terminator.

        For example, if the generated message is ``Foo`` and the
        terminator is ``\\n``, the message that will be read by the fake
        "device" would be ``Foo\\n``, and the message that will be returned is
        ``Foo``. This is where reading should stop. If it didn't, well,
        that terminator wouldn't be much use as a terminator.

        Now, for a more interesting case, consider a randomly-generated
        message with the terminator inside it. Consider the message
        ``\\r\\n`` and the terminator ``F\\r\\n``. In this case, the data to
        be read by the fake "device: would be ``\\r\\n\\r\\n``. However,
        we only want to read out ``F``, as the first instance of the
        terminator stops there.

        This method takes care of the required stripping.

        I don't need to check whether the match is found because I append
        the terminator to the message before checking it.

        :param message: The message to read, provided by Hypothesis
        :param terminator: The terminator at which to stop reading
        :return: The characters preceding the first instance of the terminator
        """
        match = re.match(
            r'^(.|\n)*?(?={0})'.format(re.escape(terminator)),
            message + terminator
        )
        return match.group(0)
