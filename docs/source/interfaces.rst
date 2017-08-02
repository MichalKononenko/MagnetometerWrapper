API Documentation
=================

The program is entirely document-able using the interfaces defined in the
``interfaces`` module. The abstract classes contained in that package should
be used to specify all interactions between objects.

..
    The automodule format below should be used to call the automodule
    directive for all modules for which automatic documentation is to be generated.
    The ``:members:`` option will document all methods in a class that do not
    start with ``_``. The ``:special-members:`` option documents all the methods
    that start with ``__``.

..
    The exclude-members option will omit documentation of these attributes. I
    decided to avoid documenting __dict__ because calls to __dict__ shouldn't be
    done directly. Instead, the object's API should be used to mutate the
    object's namespace. The __dict__ holds all the attributes and methods of the
    object, with the key of that dictionary being a string matching the name of
    the attribute

..
    __weakref__ should also be omitted. This contains a list of all the weak
    references that this object holds. Interaction with weak references to any
    objects in this project should be done using the ``weakref`` module. Using
    weak references is beyond the scope of this documentation, and so these
    members should be omitted.

..
    __module__ holds the name of the module where the object resides. I don't
    want this in my documentation, as it's unnecessary clutter

Device Communicator
-------------------

.. automodule:: magnetometer_wrapper.interfaces.device_communicator
    :members:
    :undoc-members:
    :special-members:
    :exclude-members: __dict__, __weakref__, __module__

Serial Communicator
-------------------

.. automodule:: magnetometer_wrapper.interfaces.serial_communicator
    :members:
    :undoc-members:
    :special-members:
    :exclude-members: __dict__, __weakref__, __module__

Magnetometer
------------

.. automodule:: magnetometer_wrapper.interfaces.magnetometer
    :members:
    :undoc-members:
    :special-members:
    :exclude-members: __dict__, __weakref__, __module__
