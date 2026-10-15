#line following algorithms
#wheel diameter = 65mm
#axle distance = 150mm

import motion




class line_follow_algorithms_fourline():
    far_right = 
    middle_right = 
    middle_left =
    far_left =

    left_turn_signal = far_left and middle_left and not(far_right or middle_right)
    right_turn_signal = far_right and middle_right and not(far_left or middle_left)
    t_juncion_signal = far_left and middle_left and far_right and middle_right

    def left_turn():
        motion.turn_left_90(left_motor, right_motor, turn_time=0.5, speed=30,
                 left_inverted=False, right_inverted=False)

    def right_turn():
        motion.turn_right_90(left_motor, right_motor, turn_time=0.5, speed=30,
                 left_inverted=False, right_inverted=False)

    def left_tap():


