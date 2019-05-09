from proximity_sensor import ProximitySensor
from robot_base import RobotBase
from smart_car_motor_controller import SmartCarMotorController

motor_controller = SmartCarMotorController()

front_left_ir_sensor = ProximitySensor(name='front_left_ir', pin=5)
front_right_ir_sensor = ProximitySensor(name='front_right_ir', pin=6)

sensors = [front_left_ir_sensor, front_right_ir_sensor]

wheel_separation = 0.1
max_speed = 0.2

base = RobotBase(wheel_separation, max_speed, motor_controller, sensors)

