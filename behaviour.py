from abc import abstractmethod


class Behaviour:

    def __init__(self, priority):
        self.__priority = priority

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, value):
        self.__priority = value

    @abstractmethod
    def act(self, sensors=None):
        pass
