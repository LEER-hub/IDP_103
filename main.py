import config #defining sensors
from machine import Pin, PWM
from utime import sleep,ticks_ms, ticks_diff
import motion
from line_follower import nodes, line_follow_algorithms_fourline
from servo import dropoff,pickup,open_gripper

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
robot_heading = 1 # compass[0] is north so robot begins north
path = ["c0","s_e","r0","j_la3","la3","j_la3","j_la4","r1","r2","b2l","r2","r1","j_la4","j_la3","r0","s_e","c0"]
tight_nodes = tuple(prefix + str(number) for prefix in ("c", "r", "l") for number in range(1, 7))
drop_nodes = tuple(node for node in nodes if node.endswith(("u", "l")))
short_nodes = ("la1", "la2", "la3", "la4")
node_counter = 0
start = ticks_ms()
open_gripper()
try:
    while True:
        left_turn_signal, right_turn_signal, t_junction_signal, too_left_signal, too_right_signal, no_path_signal = line_follow_algorithms_fourline(
        config.far_left_sensor.value(),
        config.middle_left_sensor.value(),
        config.middle_right_sensor.value(),
        config.far_right_sensor.value(),
    )
        if (left_turn_signal or right_turn_signal or t_junction_signal) and (ticks_diff(ticks_ms(),start) > 300):
            node_counter += 1
            current_node = path[node_counter]
            previous_node = path[node_counter -1]
            if node_counter  == len(path) - 1:
                motion.stop()
                break
            next_node = path[node_counter + 1]
            robot_aim = nodes[current_node][next_node]
            robot_turn_index = (compass.index(robot_aim)-robot_heading) % 4
            if robot_turn_index == 0:
                motion.forward()
            elif robot_turn_index == 1:
                if current_node in ("c1", "l1", "r1"):
                    motion.turn_right_90()
                elif (current_node in tight_nodes) and (previous_node in drop_nodes):
                    motion.turn_right_90()
                    node_counter += 1
                else:
                    motion.turn_right_90()
                robot_heading += 1
            elif robot_turn_index == 2:
                if current_node in short_nodes:
                    motion.stop
                    pickup()
                    motion.short_turn_180()
                else:
                    motion.turn_180()
                robot_heading += 2
            elif robot_turn_index == 3:
                if current_node == ("c1", "l1", "r1"):
                    motion.turn_left_90()
                elif (current_node in tight_nodes) and (previous_node in drop_nodes):
                    motion.turn_left_90()
                    node_counter += 1
                else:
                    motion.turn_left_90()
                robot_heading -=1
            start = ticks_ms()

        elif no_path_signal and path[node_counter] in tight_nodes:
            node_counter += 1
            current_node = path[node_counter]
            if node_counter  == len(path) - 1:
                motion.stop()
                break
            else:
                motion.turn_180()
                robot_heading += 2


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
