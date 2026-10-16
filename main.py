import line_follower
import config
from machine import Pin, PWM
from utime import sleep
import motion


'''

try:
    while True:
        turn_left_90, turn_right_90, t_junction = (
            line_follower.line_follow_algorithms_fourline(
                config.far_left_sensor.value() == 0,
                config.middle_left_sensor.value() == 0,
                config.middle_right_sensor.value() == 0,
                config.far_right_sensor.value() == 0,
            )
        )
        if turn_left_90:
            motion.forward(time=0.5)
            motion.turn_left_90()
        elif turn_right_90:
            motion.forward(time=0.5)
            motion.turn_right_90()
        elif t_junction:
            motion.forward()
        else:
            motion.forward()
finally:
    motion.stop()

'''
motion.turn_left_90(turn_time = 1.5)
sleep(1)
motion.turn_right_90(turn_time = 1.5)