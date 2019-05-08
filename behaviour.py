from abc import abstractmethod


class Behaviour:
    """
    Abstract base class for behaviours.

    Behaviours have a priority, a name and a get_action.
    The arbitrator calls get_action to allow the behaviour
    to return a command, then calls winner to inform the
    behaviour whether it has control or not. Priorities
    start from zero as the lowest priority.

    """
    def __init__(self, priority, name):
        self.__priority = priority
        self.__name = name

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, value):
        self.__priority = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @abstractmethod
    def get_action(self, sensors=None):
        return None

    @abstractmethod
    def winner(self, winner=False):
        pass
