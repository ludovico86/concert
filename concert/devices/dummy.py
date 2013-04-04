'''
Created on Mar 14, 2013

@author: farago
'''
import random
import time
from concert.base import Device, Parameter
from concert.asynchronous import async


class DummyDevice(Device):
    """A dummy device."""
    def __init__(self):
        parameter = Parameter('value', self._get_value, self._set_value)
        super(DummyDevice, self).__init__([parameter])
        self._value = None

    def _get_value(self):
        """Get the real value."""
        return self._value

    def _set_value(self, value):
        """The real value setter."""
        time.sleep(random.random())
        self._value = value

    @async
    def do_nothing(self):
        pass
