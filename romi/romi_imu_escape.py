from enum import Enum
from behaviours.behaviour import Behaviour
from motion_command import MotionCommand
from timeout import Timeout


class State(Enum):
    WAITING_TO_START = 1
    REVERSING = 2
    TURNING = 3


class RomiImuEscape(Behaviour):
    """
    Escape behaviour. Moves the robot back then turns.
    """

    def __init__(self, priority):
        super(RomiImuEscape, self).__init__(priority, 'imu_escape')
        self._state = State.WAITING_TO_START
        self._timeout = Timeout()
        self._clear_sensors()
        self._turn_right = False

    def _clear_sensors(self):
        self._pitch = 0.0
        self._roll = 0.0

    def _set_sensors(self, sensors):
        self._clear_sensors()
        for sensor in sensors:
            if sensor.name == 'imu':
                self._pitch = sensor.value[0]
                self._roll = sensor.value[1]

    def get_action(self, sensors=None):
        self._set_sensors(sensors)

        if self._state == State.WAITING_TO_START:
            # Flat, do nothing
            if abs(self._pitch) < 0.2 and abs(self._roll) < 0.2:
                return None

            # Not flat, use roll to set direction of turn.
            # We're going to always head down hill if tilted
            if self._roll < -0.2 :
                self._turn_right = False
            elif self._roll > 0.2:
                self._turn_right = True
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
