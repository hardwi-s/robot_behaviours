#! /usr/bin/python3

import time

from arbitrator import Arbitrator
from behaviours.cruise import Cruise
from motion_command import MotionCommand
from romi.romi_escape import RomiEscape
from romi.romi_robot_base import RomiRobotBase
from romi.a_star import AStar
from behaviours.teleop_keys import TeleopKeys
from romi.romi_encoder_sensor import RomiEncoderSensor
from switch_sensor import SwitchSensor

wheel_separation = 0.133  # metres
max_speed = 0.61  # m/sec

a_star = AStar()

left_bumper = SwitchSensor(name='left_bumper', pin=27)
right_bumper = SwitchSensor(name='right_bumper', pin=22)
sensors = [RomiEncoderSensor("encoders", a_star), left_bumper, right_bumper]
base = RomiRobotBase(wheel_separation, max_speed, sensors, a_star)

cruise_command = MotionCommand(0.2, 0.0)
cruise_behaviour = Cruise(0, cruise_command)
teleop_keys_behaviour = TeleopKeys(0)
escape_behaviour = RomiEscape(1)

behaviours = [teleop_keys_behaviour, escape_behaviour]

arbitrator = Arbitrator(behaviours)

while True:
    try:
        sensors = base.read_sensors()
        # for sensor in sensors:
        #    print(sensor.name + " " + str(sensor.value))
        command = arbitrator.arbitrate(sensors)
        # print(arbitrator.get_winning_behaviour().name)
        base.do_motion_command(command)
        time.sleep(0.1)
    except KeyboardInterrupt:
        teleop_keys_behaviour.stop()
        break

command = MotionCommand()
base.do_motion_command(command)
