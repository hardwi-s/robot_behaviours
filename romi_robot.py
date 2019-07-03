#! /usr/bin/python3

import time

from arbitrator import Arbitrator
from cruise import Cruise
from escape import Escape
from motion_command import MotionCommand
from romi_robot_base import RomiRobotBase
from a_star import AStar
from teleop_keys import TeleopKeys

sensors = []

wheel_separation = 0.133  # metres
max_speed = 0.61  # m/sec

a_star = AStar()
base = RomiRobotBase(wheel_separation, max_speed, sensors, a_star)

cruise_command = MotionCommand(0.2, 0.0)
cruise_behaviour = Cruise(0, cruise_command)
teleop_keys_behaviour = TeleopKeys(0)
escape_behaviour = Escape(1)

behaviours = [teleop_keys_behaviour, escape_behaviour]

arbitrator = Arbitrator(behaviours)

while True:
    try:
        sensors = base.read_sensors()
        for sensor in sensors:
            print(sensor.name + " " + str(sensor.value))
        command = arbitrator.arbitrate(sensors)
        # print(arbitrator.get_winning_behaviour().name)
        base.do_motion_command(command)
        time.sleep(0.1)
    except KeyboardInterrupt:
        break

command = MotionCommand()
base.do_motion_command(command)
