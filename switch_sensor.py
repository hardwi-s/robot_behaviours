from time import sleep

from gpiozero import DigitalInputDevice


class SwitchSensor(DigitalInputDevice):
    """
    Class for switch sensors, inherits from
    gpiozero DigitalInputDevice.
    """
    def __init__(self, name, pin, pin_factory=None):
        super().__init__(pin=pin, pull_up=True, pin_factory=pin_factory)
        self._name = name

    @property
    def value(self):
        return super().value

    @property
    def name(self):
        return self._name


if __name__ == "__main__":
    left_sensor = SwitchSensor(name='left_switch', pin=27)
    right_sensor = SwitchSensor(name='right_switch', pin=22)

    while True:
        print(left_sensor.name + " " + str(left_sensor.value))
        print(right_sensor.name + " " + str(right_sensor.value))
        sleep(0.5)
