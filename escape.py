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
        self.__state = State.WAITING_TO_START
        self.__start_time = 0.0
        self.__clear_sensors()
        self.__turn_right = False

    def __clear_sensors(self):
        self.__fl_set = False
        self.__fr_set = False
        self.__f_set = False

    def __set_sensors(self, sensors):
        self.__clear_sensors()
        for sensor in sensors:
            if sensor.value != 0:
                if sensor.name == 'front_left_ir':
                    self.__fl_set = True
                elif sensor.name == 'front_right_ir':
                    self.__fr_set = True
                elif sensor.name == 'front_ir':
                    self.__f_set = True

    def __random_turn(self):
        return random() > 0.5

    def get_action(self, sensors=None):
        self.__set_sensors(sensors)

        if self.__state == State.WAITING_TO_START:
            if self.__fl_set:
                self.__turn_right = True
            elif self.__fr_set:
                self.__turn_right = False
            elif self.__f_set:
                self.__turn_right = self.__random_turn()
            return MotionCommand(-0.1, 0)

        if self.__state == State.REVERSING:
            return MotionCommand(-0.1, 0)

    def winner(self, winner=False):
        if not winner:
            self.__state = State.WAITING_TO_START
        elif self.__state == State.WAITING_TO_START:
            self.__start_time = time.monotonic()
            self.__state = State.REVERSING
        elif self.__state == State.REVERSING:



