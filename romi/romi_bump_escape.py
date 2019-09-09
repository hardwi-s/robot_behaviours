from enum import Enum
from behaviours.behaviour import Behaviour
from motion_command import MotionCommand
from timeout import Timeout


class State(Enum):
    WAITING_TO_START = 1
    REVERSING = 2
    TURNING = 3


class RomiBumpEscape(Behaviour):
    """
    Escape behaviour. Moves the robot back then turns.
    """

    def __init__(self, priority):
        super(RomiBumpEscape, self).__init__(priority, 'bump_escape')
        self._state = State.WAITING_TO_START
        self._timeout = Timeout()
        self._clear_sensors()
        self._turn_right = False

    def _clear_sensors(self):
        self._fl_set = False
        self._fr_set = False

    def _set_sensors(self, sensors):
        self._clear_sensors()
        for sensor in sensors:
            if sensor.name == 'left_bumper':
                self._fl_set = sensor.value
            elif sensor.name == 'right_bumper':
                self._fr_set = sensor.value

    def _is_sensor_active(self):
        return self._fl_set or self._fr_set

    def get_action(self, sensors=None):
        self._set_sensors(sensors)

        if self._state == State.WAITING_TO_START:
            if not self._is_sensor_active():
                return None
            if self._fl_set:
                self._turn_right = True
            elif self._fr_set:
                self._turn_right = False
            return MotionCommand(-0.2, 0)

        elif self._state == State.REVERSING:
            return MotionCommand(-0.2, 0)

        elif self._state == State.TURNING and self._turn_right:
            return MotionCommand(0, -1.5)
        elif self._state == State.TURNING and not self._turn_right:
            return MotionCommand(0, 1.5)

        return None

    def winner(self, winner=False):
        if not winner:
            self._state = State.WAITING_TO_START

        elif self._state == State.WAITING_TO_START:
            self._timeout.start(1)
            self._state = State.REVERSING

        elif self._state == State.REVERSING and self._timeout.is_expired():
            self._timeout.start(0.5)
            self._state = State.TURNING

        elif self._state == State.TURNING and self._timeout.is_expired():
            self._state = State.WAITING_TO_START
