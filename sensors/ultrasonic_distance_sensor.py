import time

from gpiozero import DistanceSensor


class UltrasonicDistanceSensor(DistanceSensor):
    def __init__(self, name, echo, trigger, pin_factory=None):
        super().__init__(echo=echo, trigger=trigger, pin_factory=pin_factory)
        self._name = name

    def get_value(self):
        return super().distance

    def get_name(self):
        return self._name


if __name__ == "__main__":
    distance_sensor = UltrasonicDistanceSensor(name='distance', echo=19, trigger=18)

    while True:
        print(distance_sensor.get_name + " " + str(distance_sensor.get_value))
        time.sleep(0.5)
