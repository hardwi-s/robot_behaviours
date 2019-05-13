from gpiozero import DigitalInputDevice


class ProximitySensor(DigitalInputDevice):
    """
    Class for digital proximity sensors, inherits from
    gpiozero DigitalInputDevice.
    """
    def __init__(self, name, pin, pin_factory=None):
        super().__init__(pin=pin, pull_up=False, pin_factory=pin_factory)
        self._name = name

    @property
    def name(self):
        return self._name
