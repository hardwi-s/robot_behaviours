#! /usr/bin/python3

import time

from arbitrator import Arbitrator
from cruise import Cruise
from escape import Escape
from romi_robot_base import RomiRobotBase
from a_star import AStar

sensors = []

wheel_separation = 0.133
max_speed = 200

a_star = AStar()
base = RomiRobotBase(wheel_separation, max_speed, sensors, a_star)

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
