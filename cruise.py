from behaviour import Behaviour
from motion_command import MotionCommand


class Cruise(Behaviour):
    def __init__(self, priority):
        super(Cruise, self).__init__(priority, "cruise")

    def get_action(self, sensors=None):
        return MotionCommand(0.75, 0)

    def winner(self, winner=False):
        pass
