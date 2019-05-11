class Arbitrator:
    """
    Takes a list of behaviours and calls each one's get_action. If the behaviour returns
    a command then it is considered a candidate for the winning behaviour. The behaviour with the
    highest priority is considered the winner.
    """
    def __init__(self, behaviours):
        self.__behaviours = behaviours
        self.__winning_behaviour = None

    def arbitrate(self, sensors):
        """
        Iterate through behaviours and find the winner. Call back the behaviours to
        inform them of their winning status, and return the winning command
        :param sensors: Robot sensor readings
        :type sensors: list of SensorReading
        :return: Winning command
        :rtype: MotionCommand
        """
        self.__winning_behaviour = None
        winning_command = None
        for behaviour in self.__behaviours:
            command = behaviour.get_action(sensors)
            if command:
                if self.__winning_behaviour is None:
                    self.__winning_behaviour = behaviour
                    winning_command = command
                else:
                    if behaviour.priority > self.__winning_behaviour.priority:
                        self.__winning_behaviour = behaviour
                        winning_command = command

        for behaviour in self.__behaviours:
            if behaviour is self.__winning_behaviour:
                behaviour.winner(True)
            else:
                behaviour.winner(False)

        return winning_command

    def get_winning_behaviour(self):
        return self.__winning_behaviour
