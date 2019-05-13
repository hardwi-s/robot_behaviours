class Arbitrator:
    """
    Takes a list of behaviours and calls each one's get_action. If the behaviour returns
    a command then it is considered a candidate for the winning behaviour. The behaviour with the
    highest priority is considered the winner.
    """
    def __init__(self, behaviours):
        self._behaviours = behaviours
        self._winning_behaviour = None

    def arbitrate(self, sensors):
        """
        Iterate through behaviours and find the winner. Call back the behaviours to
        inform them of their winning status, and return the winning command
        :param sensors: Robot sensor readings
        :type sensors: list of SensorReading
        :return: Winning command
        :rtype: MotionCommand
        """
        self._winning_behaviour = None
        winning_command = None
        for behaviour in self._behaviours:
            command = behaviour.get_action(sensors)
            if command:
                if self._winning_behaviour is None:
                    self._winning_behaviour = behaviour
                    winning_command = command
                else:
                    if behaviour.priority > self._winning_behaviour.priority:
                        self._winning_behaviour = behaviour
                        winning_command = command

        for behaviour in self._behaviours:
            if behaviour is self._winning_behaviour:
                behaviour.winner(True)
            else:
                behaviour.winner(False)

        return winning_command

    def get_winning_behaviour(self):
        return self._winning_behaviour
