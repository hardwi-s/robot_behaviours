from behaviours.behaviour import Behaviour
from motion_command import MotionCommand
from enum import Enum


class State(Enum):
    WAITING_TO_START = 1
    POINTING = 2
    MOVING = 3
    ARRIVED = 4
    FINISHED = 5


class GoToWaypoints(Behaviour):
    """
    Visit a list of waypoints.
    """
    def __init__(self, priority, waypoints):
        super(GoToWaypoints, self).__init__(priority, "go_to_waypoints")
        self._waypoints = waypoints
        self._command = MotionCommand()
        self._state = State.WAITING_TO_START

    def get_action(self, sensors=None):
        return self._command

    def winner(self, winner=False):
        pass
