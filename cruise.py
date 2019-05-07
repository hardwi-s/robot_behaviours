from behaviour import Behaviour
from motion_command import MotionCommand


class Cruise(Behaviour):

    def __init__(self, priority):
        super(Cruise, self).__init__(priority, "cruise")

    def act(self, sensors=None):
        return MotionCommand(75, 0)
