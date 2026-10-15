#line following algorithms
#wheel diameter = 65mm
#axle distance = 150mm

import motion
import config




def line_follow_algorithms_fourline(far_left_sensor, middle_left_sensor, middle_right_sensor, far_right_sensor):

    left_turn_signal = far_left_sensor and middle_left_sensor and not(far_right_sensor or middle_right_sensor)
    right_turn_signal = far_right_sensor and middle_right_sensor and not(far_left_sensor or middle_left_sensor)
    t_junction_signal = far_left_sensor and middle_left_sensor and far_right_sensor and middle_right_sensor
    return left_turn_signal, right_turn_signal, t_junction_signal



