import config  # defining sensors
import _thread
from machine import Pin, PWM
from utime import sleep, ticks_ms, ticks_diff
import motion
from line_follower import nodes, line_follow_algorithms_fourline
from on_off_switch import check_switch
from paths import (tight_nodes, short_nodes, nodeskip, get_turn, breadth_first_search_algo, plan_available_dropoff
,right_pickup_nodes, left_pickup_nodes, available_dropoff_nodes_right_lower, available_dropoff_nodes_right_upper, available_dropoff_nodes_left_lower, available_dropoff_nodes_left_upper, bay_unavailable
,right_nodes)


# field mapping implementation
robot_heading = 1  # compass[0] is north so robot begins east
path = []
node_counter = 0
current_node = "c0"
path = breadth_first_search_algo(current_node, "la3")
start = ticks_ms()
carrying = False
target_bay = None
try:

    config.servo1.set_angle(137.5)
    config.servo2.set_angle(0)
    _thread.start_new_thread(motion.amber_led_toggle, ())
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

        junction_detected = left_turn_signal or right_turn_signal or t_junction_signal
        endpoint_detected = no_path_signal and path[node_counter] in tight_nodes
        if (junction_detected or endpoint_detected) and ticks_diff(ticks_ms(), start) > 300:
            node_counter += 1
            current_node = path[node_counter]
            previous_node = path[node_counter - 1]
            if node_counter == len(path) - 1:
                motion.stop()

                if current_node in ("la1", "la2", "la3", "la4") and not carrying:
                    motion.stop()
                    motion.pickup()
                    carrying = True

                    polarity = magnetometer.read()
                    side = "right" if current_node in ("la3", "la4") else "left"
                    path, target_bay = plan_available_dropoff(
                        current_node, polarity, side
                    )
                    node_counter = 0

                elif target_bay is not None and current_node == target_bay:
                    if distance_sensor.distance_cm() < 10:
                        bay_unavailable(target_bay)
                        path, target_bay = plan_available_dropoff(
                            current_node, polarity, side
                        )
                        # Keep holding the box while trying the next bay.
                        node_counter = 0
                    else:
                        motion.dropoff()
                        bay_unavailable(target_bay)
                        carrying = False
                        target_bay = None

                        pickup_node = "la4" if side == "right" else "la1"
                        path = breadth_first_search_algo(current_node, pickup_node)
                        node_counter = 0

                else:
                    break

            if not path or node_counter + 1 >= len(path):
                motion.stop()
                break

            next_node = path[node_counter + 1]
            robot_turn_index = get_turn(current_node, next_node, robot_heading)
            if robot_turn_index == 0:
                motion.forward()
            elif robot_turn_index == 1:
                motion.turn_right_90()
                if nodeskip(previous_node, current_node, next_node):
                    node_counter += 1
                robot_heading += 1
            elif robot_turn_index == 2:
                if current_node in short_nodes:
                    side = "right" if current_node in right_pickup_nodes else "left"
                    motion.short_turn_180()
                else:
                    motion.turn_180()
                robot_heading += 2
            elif robot_turn_index == 3:
                motion.turn_left_90()
                if nodeskip(previous_node, current_node, next_node):
                    node_counter += 1
                robot_heading -= 1
            start = ticks_ms()

        else:
            motion.forward()
            if too_left_signal:
                motion.right_tap()
            elif too_right_signal:
                motion.left_tap()
finally:
    motion.stop()


# auto mapping plan
# robot remembers the last node it passed alongside the direction it is facing after executing a motion on that node
# e.g. lets say it detects node c0 then it executes a right turn then the heading updates and the next node is calculated
# this repeats
# eventually we want to create a node path so the program can tell what direction it needs to turn to at what node to head to the next
# a node detection is triggered by the line_follower.py's conditions of left turn signal right turn signal t junction signal etc


