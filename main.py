import line_follower
import config
from machine import Pin, PWM
from utime import sleep
import motion
try:
    while True:
        left_turn, right_turn, t_junction = (
            line_follower.line_follow_algorithms_fourline(
                config.far_left_sensor.value() == 0,
                config.middle_left_sensor.value() == 0,
                config.middle_right_sensor.value() == 0,
                config.far_right_sensor.value() == 0,
            )
        )
        if left_turn:
            motion.turn_left_90(turn_time=2)
        elif right_turn:
            motion.turn_right_90(turn_time=2)
        elif t_junction:
            motion.forward()
        else:
            motion.forward()
finally:
    motion.stop()