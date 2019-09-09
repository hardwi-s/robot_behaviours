#! /usr/bin/python3

import time

from arbitrator import Arbitrator
from behaviours.cruise import Cruise
from romi.romi_pose_sensor import RomiPoseSensor
from motion_command import MotionCommand
from romi.romi_bump_escape import RomiBumpEscape
from romi.romi_robot_base import RomiRobotBase
from romi.a_star import AStar
from behaviours.teleop_keys import TeleopKeys
from romi.romi_encoder_sensor import RomiEncoderSensor
from romi.romi_usonic_escape import RomiUsonicEscape
from sensors.sensors import Sensors
from sensors.ultrasonic_distance_sensor import UltrasonicDistanceSensor
from simple_server import Server
from sensors.switch_sensor import SwitchSensor

wheel_separation = 0.133  # metres
max_speed = 0.61  # m/sec

a_star = AStar()

base = RomiRobotBase(wheel_separation, max_speed, a_star)

left_bumper = SwitchSensor(name='left_bumper', pin=27)
right_bumper = SwitchSensor(name='right_bumper', pin=22)
distance = UltrasonicDistanceSensor(name='distance', echo=19, trigger=18)
encoders = RomiEncoderSensor('encoders', a_star)
pose_sensor = RomiPoseSensor('pose', base=base, encoders=encoders)
sensors = Sensors(sensors=[pose_sensor, encoders, left_bumper, right_bumper, distance])


cruise_command = MotionCommand(0.2, 0.0)
cruise_behaviour = Cruise(0, cruise_command)
#teleop_keys_behaviour = TeleopKeys(0)
bump_escape_behaviour = RomiBumpEscape(2)
usonic_escape_behaviour = RomiUsonicEscape(1)

#behaviours = [teleop_keys_behaviour, escape_behaviour]
behaviours = [cruise_behaviour, usonic_escape_behaviour, bump_escape_behaviour]
arbitrator = Arbitrator(behaviours)

server = Server(host='192.168.1.101', port=65432)
server.start()

while True:
    try:
        sensor_readings = sensors.read_sensors()
        server.update(sensor_readings)
        for sensor_reading in sensor_readings:
            print(sensor_reading.name + " " + str(sensor_reading.value))
        command = arbitrator.arbitrate(sensor_readings)
        # print(arbitrator.get_winning_behaviour().name)
        base.do_motion_command(command)

        time.sleep(0.1)

    except KeyboardInterrupt:
        # teleop_keys_behaviour.stop()
        server.stop()
        break

command = MotionCommand()
base.do_motion_command(command)
