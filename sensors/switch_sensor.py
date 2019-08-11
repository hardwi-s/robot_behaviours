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

    def get_value(self):
        return super().value

    def get_name(self):
        return self._name


if __name__ == "__main__":
    left_sensor = SwitchSensor(name='left_switch', pin=27)
    right_sensor = SwitchSensor(name='right_switch', pin=22)

    while True:
        print(left_sensor.get_name + " " + str(left_sensor.get_value))
        print(right_sensor.get_name + " " + str(right_sensor.get_value))
        sleep(0.5)
