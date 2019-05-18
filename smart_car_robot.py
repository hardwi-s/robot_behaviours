import time

from arbitrator import Arbitrator
from cruise import Cruise
from escape import Escape
from proximity_sensor import ProximitySensor
from robot_base import RobotBase
from smart_car_motor_controller import SmartCarMotorController

motor_controller = SmartCarMotorController()

front_left_ir_sensor = ProximitySensor(name='front_left_ir', pin=20)
front_right_ir_sensor = ProximitySensor(name='front_right_ir', pin=21)
front_ir_sensor = ProximitySensor(name='front_ir', pin=26)

sensors = [front_ir_sensor, front_left_ir_sensor, front_right_ir_sensor]

wheel_separation = 0.1
max_speed = 0.2

base = RobotBase(wheel_separation, max_speed, motor_controller, sensors)

cruise_behaviour = Cruise(0)
escape_behaviour = Escape(1)

behaviours = [cruise_behaviour, escape_behaviour]

arbitrator = Arbitrator(behaviours)

while True:
    sensors = base.read_sensors()
    for sensor in sensors:
        print(sensor.name + " " + str(sensor.value))
    command = arbitrator.arbitrate(sensors)
    print(arbitrator.get_winning_behaviour().name)
    base.do_motion_command(command)
    time.sleep(0.1)
