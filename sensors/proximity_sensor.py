from time import sleep

from gpiozero import DigitalInputDevice


class ProximitySensor(DigitalInputDevice):
    """
    Class for digital proximity sensors, inherits from
    gpiozero DigitalInputDevice.
    """
    def __init__(self, name, pin, pin_factory=None):
        super().__init__(pin=pin, pull_up=False, pin_factory=pin_factory)
        self._name = name

    def get_value(self):
        return not super().value

    def get_name(self):
        return self._name


if __name__ == "__main__":
    front_left_ir_sensor = ProximitySensor(name='front_left_ir', pin=20)
    front_right_ir_sensor = ProximitySensor(name='front_right_ir', pin=21)
    front_ir_sensor = ProximitySensor(name='front_ir', pin=26)

    while True:
        print(front_left_ir_sensor.get_name() + " " + str(front_left_ir_sensor.get_value()))
        print(front_right_ir_sensor.get_name() + " " + str(front_right_ir_sensor.get_value()))
        print(front_ir_sensor.get_name() + " " + str(front_ir_sensor.get_value()))
        sleep(0.5)
