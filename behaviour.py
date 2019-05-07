from abc import abstractmethod


class Behaviour:

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
    def act(self, sensors=None):
        return None
