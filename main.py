import config #defining sensors
import _thread
from machine import Pin, PWM
from utime import sleep,ticks_ms, ticks_diff
import motion
from line_follower import nodes, line_follow_algorithms_fourline
from on_off_switch import check_switch
from paths import tight_nodes,short_nodes,nodeskip,get_turn


#field mapping implementation
robot_heading = 1 # compass[0] is north so robot begins east
path = ["c0","s_e","r0","j_la3","la3","j_la3","j_la4","r1","r2","b2l","r2","r1","j_la4","j_la3","r0","s_e","c0",
        "s_w","l0","j_la2","la2", "j_la2","j_la1","l1","l2","a2l","l2","l1","j_la1","j_la2","l0","s_w","c0",
        "s_e","r0","j_la3","j_la4","la4","j_la4","r1","r2","r3","b3l","r3","r2","r1","j_la4","j_la3","r0","s_e","c0",
        "s_w","l0","j_la1","la1","j_la1","l1","a1l","l1","j_la1","j_la2","l0","s_w","c0"]
node_counter = 0
start = ticks_ms()
try:

    config.servo1.set_angle(150)
    config.servo2.set_angle(0)
    while True:
        if not check_switch():
            motion.stop()
            start = ticks_ms()
            sleep(0.01)
            continue

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
            robot_turn_index = get_turn(current_node, next_node, robot_heading)
            if robot_turn_index == 0:
                motion.forward()
            elif robot_turn_index == 1:
                motion.turn_right_90()
                if nodeskip(previous_node,current_node,next_node):
                    node_counter += 1 
                robot_heading += 1
            elif robot_turn_index == 2:
                if current_node in short_nodes:
                    motion.stop()
                    motion.pickup()
                    motion.short_turn_180()
                else:
                    motion.turn_180()
                robot_heading += 2
            elif robot_turn_index == 3:
                motion.turn_left_90()
                if nodeskip(previous_node,current_node,next_node):
                    node_counter += 1
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

