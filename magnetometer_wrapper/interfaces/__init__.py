"""
Contains the abstract base classes to be used as interfaces for the project.

In order to create more loosely-coupled Python code, as well as take full
advantage of the new type hinting syntax, this package provides a set of
base classes that can be used to define interfaces. Each class in this
package is an abstract class that raises ``NotImplementedError`` for any of
its methods. Consequently, these interfaces should be able to participate in
multiple inheritance without any fear of implementation conflicts
"""
from .device_communicator import DeviceCommunicator
from .serial_communicator import SerialCommunicator
from .magnetometer import Magnetometer
