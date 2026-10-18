import line_follower
import config
from machine import Pin, PWM
from utime import sleep
import motion

'''
try:
    while True:
        left_turn_signal, right_turn_signal, t_junction_signal = line_follower.line_follow_algorithms_fourline(
        config.far_left_sensor.value() == 0,
        config.middle_left_sensor.value() == 0,
        config.middle_right_sensor.value() == 0,
        config.far_right_sensor.value() == 0,
    )
        if left_turn_signal:
            motion.turn_left_90()
        elif right_turn_signal:
            motion.turn_right_90()
        elif t_junction_signal:
            motion.forward()
        else:
            motion.forward()
finally:
    motion.stop()
'''

left_detection_counter = 0
right_detection_counter = 0
crossroad_detection_counter = 0
stepcounter = 0

try:
    while True:
        left_turn_signal, right_turn_signal, t_junction_signal, too_left_signal, too_right_signal = line_follower.line_follow_algorithms_fourline(
            config.far_left_sensor.value(),
            config.middle_left_sensor.value(),
            config.middle_right_sensor.value(),
            config.far_right_sensor.value() 
        )

        # Return to the outer loop after each correction to reread sensors.
        if too_left_signal:
            motion.right_tap()
        elif too_right_signal:
            motion.left_tap()
        elif stepcounter == 0:
            motion.forward()
            if t_junction_signal:
                motion.forward()
                sleep(3)
                stepcounter += 1

        elif stepcounter == 1:
            if left_turn_signal:
                motion.turn_left_90()
                stepcounter += 1
        elif stepcounter == 2:
            if left_turn_signal:
                motion.turn_left_90()
                stepcounter += 1
        elif stepcounter == 3:
            if t_junction_signal:
                motion.stop()
                sleep(1)
                motion.turn_180()
                stepcounter += 1
        elif stepcounter == 4:
            if left_turn_signal:
                motion.turn_left_90()
                stepcounter += 1
        elif stepcounter == 5:
            if left_turn_signal:
                motion.forward()
                stepcounter += 1
        else:
            motion.forward()
finally:
    motion.stop()

#algo for line following:
#1. ignore first crossroad (t unction) and go straight
#2. when left turn signal, turn left 90 degrees
#3 turn left again on the left signal
#4. stop at the next crossroad 
#5. turn around 180 degrees
#6 take the next left turn
#7 go striaght and ignore the next left but take the left after that
#8 go straight around 3 seconds
#9 turn around 180 
#10 go staight
#11 turn right
    print("No turn detected.")