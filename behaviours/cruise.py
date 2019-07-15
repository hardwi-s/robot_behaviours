from behaviours.behaviour import Behaviour


class Cruise(Behaviour):
    """
    Cruise behaviour. Moves the robot in a commanded path.
    """
    def __init__(self, priority, command):
        super(Cruise, self).__init__(priority, "cruise")
        self._command = command

    def get_action(self, sensors=None):
        return self._command

    def winner(self, winner=False):
        pass
