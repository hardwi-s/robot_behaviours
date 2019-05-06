from behaviour import Behaviour
from motor_command import MotorCommand


class Cruise(Behaviour):

    def __init__(self, priority):
        super(Cruise, self).__init__(priority)

    def act(self, sensors=None):
        return MotorCommand(75, 0)
