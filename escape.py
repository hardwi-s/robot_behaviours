import time
from enum import Enum
from random import random

from behaviour import Behaviour
from motion_command import MotionCommand
from timeout import Timeout


class State(Enum):
    WAITING_TO_START = 1
    REVERSING = 2
    TURNING = 3


class Escape(Behaviour):
    """
    Escape behaviour. Moves the robot back then turns.
    """
    def __init__(self, priority):
        super(Escape, self).__init__(priority, 'escape')
        self._state = State.WAITING_TO_START
        self._timeout = Timeout()
        self._clear_sensors()
        self._turn_right = False

    def _clear_sensors(self):
        self._fl_set = False
        self._fr_set = False
        self._f_set = False

    def _set_sensors(self, sensors):
        self._clear_sensors()
        for sensor in sensors:
            if sensor.name == 'front_left_ir':
                self._fl_set = sensor.value
            elif sensor.name == 'front_right_ir':
                self._fr_set = sensor.value
            elif sensor.name == 'front_ir':
                self._f_set = sensor.value

    def _random_turn(self):
        return random() > 0.5

    def _is_sensor_active(self):
        return self._fl_set or self._fr_set or self._f_set

    def get_action(self, sensors=None):
        self._set_sensors(sensors)

        if self._state == State.WAITING_TO_START:
            if not self._is_sensor_active():
                return None
            if self._fl_set:
                self._turn_right = True
            elif self._fr_set:
                self._turn_right = False
            elif self._f_set:
                self._turn_right = self._random_turn()
            return MotionCommand(-0.4, 0)

        elif self._state == State.REVERSING:
            return MotionCommand(-0.4, 0)

        elif self._state == State.TURNING and self._turn_right:
            return MotionCommand(0, -2.5)
        elif self._state == State.TURNING and not self._turn_right:
            return MotionCommand(0, 2.5)

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



