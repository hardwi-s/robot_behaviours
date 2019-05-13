import time
from enum import Enum
from random import random

from behaviour import Behaviour
from motion_command import MotionCommand


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
        self._start_time = 0.0
        self._clear_sensors()
        self._turn_right = False

    def _clear_sensors(self):
        self._fl_set = False
        self._fr_set = False
        self._f_set = False

    def _set_sensors(self, sensors):
        self._clear_sensors()
        for sensor in sensors:
            if sensor.value != 0:
                if sensor.name == 'front_left_ir':
                    self._fl_set = True
                elif sensor.name == 'front_right_ir':
                    self._fr_set = True
                elif sensor.name == 'front_ir':
                    self._f_set = True

    def _random_turn(self):
        return random() > 0.5

    def get_action(self, sensors=None):
        self._set_sensors(sensors)

        if self._state == State.WAITING_TO_START:
            if self._fl_set:
                self._turn_right = True
            elif self._fr_set:
                self._turn_right = False
            elif self._f_set:
                self._turn_right = self._random_turn()
            return MotionCommand(-0.1, 0)

        if self._state == State.REVERSING:
            return MotionCommand(-0.1, 0)

    def winner(self, winner=False):
        if not winner:
            self._state = State.WAITING_TO_START
        elif self._state == State.WAITING_TO_START:
            self._start_time = time.monotonic()
            self._state = State.REVERSING
        elif self._state == State.REVERSING:



