from behaviour import Behaviour
from motion_command import MotionCommand


class Cruise(Behaviour):
    """
    Cruise behaviour. Moves the robot in a straight line.
    """
    def __init__(self, priority):
        super(Cruise, self).__init__(priority, "cruise")

    def get_action(self, sensors=None):
        return MotionCommand(0.1, 0)

    def winner(self, winner=False):
        pass
