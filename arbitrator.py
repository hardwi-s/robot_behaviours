class Arbitrator:
    """
    Takes a list of behaviours and calls each one's get_action. If the behaviour returns
    a command then it is considered for being the winning behaviour. The behaviour with the
    highest priority is considered the winner.
    """
    def __init__(self, behaviours):
        self.__behaviours = behaviours

    def arbitrate(self, sensors):
        winning_behaviour = None
        winning_command = None
        for behaviour in self.__behaviours:
            command = behaviour.get_action(sensors)
            if command:
                if winning_behaviour is None:
                    winning_behaviour = behaviour
                    winning_command = command
                else:
                    if behaviour.priority > winning_behaviour.priority:
                        winning_behaviour = behaviour
                        winning_command = command

        for behaviour in self.__behaviours:
            if behaviour is winning_behaviour:
                behaviour.winner(True)
            else:
                behaviour.winner(False)

        return winning_command
