from gpiozero import DigitalInputDevice


class ProximitySensor(DigitalInputDevice):

    def __init__(self, name, pin, pin_factory):
        super().__init__(pin=pin, pull_up=False, pin_factory=pin_factory)
        self.__name = name

    @property
    def name(self):
        return self.__name
