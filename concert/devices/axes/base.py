from concert.base import launch
from concert.events import type as eventtype
from concert.devices.base import State, Device


class AxisState(State):
    """Axis status."""
    STANDBY = eventtype.make_event_id()
    MOVING = eventtype.make_event_id()


class AxisMessage(object):
    """Axis message."""
    POSITION_LIMIT = eventtype.make_event_id()
    VELOCITY_LIMIT = eventtype.make_event_id()


class Axis(Device):
    """Base class for everything that moves.

    An axis is used with a *calibration* that conforms to the
    :class:`Calibration` interface to convert between user and device units.

    Exported parameters:
        - ``"position"``: Position of the axis
    """

    def __init__(self, calibration):
        super(Axis, self).__init__()

        self._state = None
        self._register('position',
                       calibration.to_user,
                       calibration.to_steps,
                       None)

    def __del__(self):
        self.stop()

    def set_position(self, position, blocking=False):
        """Set the *position* in user units."""
        self.set('position', position, blocking)

    def get_position(self):
        """Get the position in user units."""
        return self.get('position')

    def move(self, delta, blocking=False):
        """Move axis by *delta* user units."""
        new_position = self.get_position() + delta
        self.set_position(new_position, blocking)

    def stop(self, blocking=False):
        """Stop the motion."""
        launch(self._stop_real, blocking=blocking)

    @property
    def state(self):
        return self._state

    def _set_state(self, state):
        self._state = state
        self.send(self._state)

    def _stop_real(self):
        """Stop the physical axis.

        This method must be always blocking in order to provide appropriate
        events at appropriate times.

        """
        raise NotImplementedError

    def hard_position_limit_reached(self):
        raise NotImplementedError


class ContinuousAxis(Axis):
    """A movable on which one can set velocity.

    This class is inherently capable of discrete movement.

    """
    def __init__(self, position_calibration, velocity_calibration):
        super(ContinuousAxis, self).__init__(position_calibration)
        self._velocity = None
        self._velocity_calibration = velocity_calibration

        self._register('velocity',
                       velocity_calibration.to_user,
                       velocity_calibration.to_steps,
                       None)

    def set_velocity(self, velocity, blocking=False):
        """Set *velocity* of the axis."""
        self.set('velocity', velocity, blocking)

    def get_velocity(self):
        """Get current velocity of the axis."""
        return self.get('velocity')


class Calibration(object):
    """Interface to convert between user and device units."""

    def to_user(self, value):
        """Return *value* in user units."""
        raise NotImplementedError

    def to_steps(self, value):
        """Return *value* in device units."""
        raise NotImplementedError


class LinearCalibration(Calibration):
    """A linear calibration maps a number of motor steps to a real-world unit.

    *steps_per_unit* tells how many steps correspond to some unit,
    *offset_in_steps* by how many steps the device is away from some zero
    point.
    """
    def __init__(self, steps_per_unit, offset_in_steps):
        self._steps_per_unit = steps_per_unit
        self._offset = offset_in_steps

    def to_user(self, value_in_steps):
        return value_in_steps / self._steps_per_unit - self._offset

    def to_steps(self, value):
        return (value + self._offset) * self._steps_per_unit