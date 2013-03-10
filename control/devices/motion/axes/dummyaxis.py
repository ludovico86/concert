'''
Created on Mar 5, 2013

@author: farago
'''
import numpy
import time
from control.devices.motion.axes.axis import Axis, ContinuousAxis
from control.devices.motion.axes.axis import AxisState, ContinuousAxisState
from control.events import generator as eventgenerator
from control.events import type as eventtype
from control.events.event import Event


class DummyAxis(Axis):
    def __init__(self, connection, calibration, position_limit=None):
        super(DummyAxis, self).__init__(connection,
                                        calibration,
                                        position_limit)
        self._hard_limits = -100, 100
        self._position = 0

    def _stop_real(self):
        pass

    def _set_position_real(self, position):
        self._set_state(AxisState.MOVING)

        time.sleep(numpy.random.random() / 2.)

        if position < self._hard_limits[0]:
            self._position = self._hard_limits[0]
            self._set_state(AxisState.POSITION_LIMIT)
        elif position > self._hard_limits[1]:
            self._position = self._hard_limits[1]
            self._set_state(AxisState.POSITION_LIMIT)
        else:
            self._position = position
            self._set_state(AxisState.STANDBY)

    def _get_position_real(self):
        return self._position

    def _is_hard_position_limit_reached(self):
        return self._position <= self._hard_limits[0] or \
               self._position >= self._hard_limits[1]


class DummyContinuousAxis(ContinuousAxis):
    def __init__(self, connection, position_calibration, velocity_calibration,
                 position_limit=None, velocity_limit=None):

        super(DummyContinuousAxis, self).__init__(connection,
                                                  position_calibration,
                                                  velocity_calibration,
                                                  position_limit,
                                                  velocity_limit)
        self._position_hard_limits = -10, 10
        self._velocity_hard_limits = -100, 100
        self._position = 0
        self._velocity = 0

    def _stop_real(self):
        time.sleep(0.5)
        self._velocity = 0

    def _set_position_real(self, position):
        time.sleep(numpy.random.random() / 2.)

        self._position = position
        if self._position < self._position_hard_limits[0]:
            self._position = self._position_hard_limits[0]
        elif self._position > self._position_hard_limits[1]:
            self._position = self._position_hard_limits[1]

    def _get_position_real(self):
        return self._position

    def _is_hard_position_limit_reached(self):
        return self._position <= self._position_hard_limits[0] or \
               self._position >= self._position_hard_limits[1]

    def _set_velocity_real(self, velocity):
        self._set_state(AxisState.MOVING)

        time.sleep(numpy.random.random())
        self._velocity = velocity

        if self._velocity < self._velocity_hard_limits[0]:
            self._velocity = self._velocity_hard_limits[0]
            self._set_state(ContinuousAxisState.VELOCITY_LIMIT)
        elif self._velocity > self._velocity_hard_limits[1]:
            self._velocity = self._velocity_hard_limits[1]
            self._set_state(ContinuousAxisState.VELOCITY_LIMIT)
        else:
            self._set_state(AxisState.STANDBY)

    def _get_velocity_real(self):
        return self._velocity

    def _is_hard_velocity_limit_reached(self):
        return self._position <= self._velocity_hard_limits[0] or \
               self._position >= self._velocity_hard_limits[1]