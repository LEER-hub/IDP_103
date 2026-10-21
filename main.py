import config #defining sensors
from machine import Pin, PWM
from utime import sleep,ticks_ms, ticks_diff
import motion
from line_follower import nodes, line_follow_algorithms_fourline

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
        if stepcounter == 0 and t_junction_signal:
            motion.forward()
            sleep(1.2)
            stepcounter += 1
        elif stepcounter == 1 and left_turn_signal:
            motion.turn_left_90()
            stepcounter += 1
        elif stepcounter == 2 and left_turn_signal:
            motion.turn_left_90()
            stepcounter += 1
        elif stepcounter == 3 and t_junction_signal:
            motion.stop()
            sleep(1)
            motion.forward()
            sleep(1.5)
            motion.turn_180()
            stepcounter += 1
        elif stepcounter == 4 and (left_turn_signal or t_junction_signal):
            motion.turn_left_90()
            stepcounter += 1
        elif stepcounter == 5 and left_turn_signal:
            motion.forward()
            sleep(1.2)
            stepcounter += 1
        elif stepcounter == 6 and left_turn_signal:
            motion.forward()
            sleep(0.5)
            stepcounter += 1
        elif stepcounter == 7 and left_turn_signal:
            motion.turn_left_90()
            stepcounter += 1
        elif stepcounter == 8:
            motion.forward()
            sleep(3)
            motion.stop()
            stepcounter += 1
        elif stepcounter == 9:
            sleep(1)
            motion.turn_180()
            stepcounter += 1
        elif stepcounter == 10 and (right_turn_signal or t_junction_signal):
            motion.turn_right_90()
            stepcounter += 1
        elif stepcounter == 11 and right_turn_signal:
            motion.forward()
            sleep(1.0)
            stepcounter += 1
        elif stepcounter == 12 and right_turn_signal:
            motion.turn_right_90()
            stepcounter += 1
        elif stepcounter == 13 and t_junction_signal:
            motion.forward()
            sleep(3)
            motion.stop()
            sleep(30)
            stepcounter += 1
        elif too_left_signal:
                motion.right_tap()
        elif too_right_signal:
                motion.left_tap()
        else:
            motion.forward()
finally:
    motion.stop()

'''
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


compass = ["north", "east", "south", "west"]
robot_heading = 0 # compass[0] is north so robot begins north
path = ["c0","s_n","c1","c2","c3","b3u"]
node_counter = 0
start = ticks_ms()
try:
    while True:
        left_turn_signal, right_turn_signal, t_junction_signal, too_left_signal, too_right_signal = line_follow_algorithms_fourline(
        config.far_left_sensor.value(),
        config.middle_left_sensor.value(),
        config.middle_right_sensor.value(),
        config.far_right_sensor.value(),
    )
        if (left_turn_signal or right_turn_signal or t_junction_signal) and (ticks_diff(ticks_ms(),start) > 300):
            node_counter += 1
            current_node = path[node_counter]
            if node_counter  == len(path) - 1:
                motion.stop()
                break
            next_node = path[node_counter + 1]
            robot_aim = nodes[current_node][next_node]
            robot_turn_index = (compass.index(robot_aim)-robot_heading) % 4
            if robot_turn_index == 0:
                motion.forward()
            elif robot_turn_index == 1:
                motion.turn_right_90()
                robot_heading += 1
            elif robot_turn_index == 2:
                motion.turn_180()
                robot_heading += 2
            elif robot_turn_index == 3:
                motion.turn_left_90()
                robot_heading -=1
            start = ticks_ms()

        else:
            motion.forward()
            if too_left_signal:
                motion.right_tap()
            elif too_right_signal:
                motion.left_tap()
finally:
    motion.stop()



#auto mapping plan
#robot remembers the last node it passed alongside the direction it is facing after executing a motion on that node
#e.g. lets say it detects node c0 then it executes a right turn then the heading updates and the next node is calculated
#this repeats
#eventually we want to create a node path so the program can tell what direction it needs to turn to at what node to head to the next
#a node detection is triggered by the line_follower.py's conditions of left turn signal right turn signal t junction signal etc