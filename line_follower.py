#line following algorithms
#wheel diameter = 65mm
#axle distance = 150mm

# This module only interprets readings; it does not initialize or drive motors.
ZERO_CONFIRM_COUNT = 3
_last_seen = None
_zero_count = 0


def reset_line_history():
    """Call before a new run, or after an intentional turn/junction manoeuvre."""
    global _last_seen, _zero_count
    _last_seen = None
    _zero_count = 0


def line_follow_algorithms_fourline(far_left_sensor, middle_left_sensor,
                                   middle_right_sensor, far_right_sensor,
                                   tracking_state="following"):
    """Interpret one sample, ordered left to right; 1/True means white.

    Pass readings such as config.far_left_sensor.value(), NOT Pin objects.
    Call at a regular interval: the confirmation threshold counts samples.
    Pass tracking_state='turning' or 'junction' during planned manoeuvres to
    clear/suppress lost-line history. Only one robot's history is kept here.

    Returned turn/junction flags are candidates, not confirmed route geometry.
    Search flags request a small search, NOT a 90-degree turn. The caller must
    bound motor searching with a timeout and stop if no line is found.
    A nonzero sample clears the search request, but does not prove centering.
    action is one decision per sample, not a motor command. 'straight' for
    0000 is provisional: this sensor layout cannot prove that the line is
    between the inner sensors. Unknown patterns request stop_and_check.
    During planned manoeuvres action is 'manoeuvre'; the caller owns motion.
    """
    global _last_seen, _zero_count

    readings = (far_left_sensor, middle_left_sensor,
                middle_right_sensor, far_right_sensor)
    if any(value not in (0, 1) for value in readings):
        raise ValueError("Pass four 0/1 readings, not sensor Pin objects")

    left_turn_signal = far_left_sensor and middle_left_sensor and not(far_right_sensor or middle_right_sensor)
    right_turn_signal = far_right_sensor and middle_right_sensor and not(far_left_sensor or middle_left_sensor)
    t_junction_signal = far_left_sensor and middle_left_sensor and far_right_sensor and middle_right_sensor

    no_line_signal = not any(readings)
    if tracking_state != "following":
        reset_line_history()
    elif no_line_signal:
        _zero_count = min(_zero_count + 1, ZERO_CONFIRM_COUNT)
        # Keep the last detected position while all four sensors see dark.
    else:
        _zero_count = 0
        # Only isolated outer readings arm the lost-line condition.
        # Inner readings cancel it; ambiguous/branch patterns clear it too.
        if readings == (1, 0, 0, 0):
            _last_seen = "left_outer"
        elif readings == (0, 0, 0, 1):
            _last_seen = "right_outer"
        elif readings == (0, 1, 0, 0):
            _last_seen = "left_inner"
        elif readings == (0, 0, 1, 0):
            _last_seen = "right_inner"
        else:
            _last_seen = None

    search_left_signal = (tracking_state == "following"
                          and _last_seen == "left_outer"
                          and _zero_count >= ZERO_CONFIRM_COUNT)
    search_right_signal = (tracking_state == "following"
                           and _last_seen == "right_outer"
                           and _zero_count >= ZERO_CONFIRM_COUNT)

    # Select one action so ordinary straight driving cannot override searching.
    # Keep slowing during the first two all-dark samples after outer detection.
    if tracking_state != "following":
        action = "manoeuvre"
    elif search_left_signal:
        action = "search_left"
    elif search_right_signal:
        action = "search_right"
    elif left_turn_signal:
        action = "confirm_left_branch"
    elif right_turn_signal:
        action = "confirm_right_branch"
    elif t_junction_signal:
        action = "confirm_junction"
    elif readings == (0, 1, 0, 0):
        action = "adjust_left"
    elif readings == (0, 0, 1, 0):
        action = "adjust_right"
    elif (readings in ((1, 0, 0, 0), (0, 0, 0, 1))
          or (no_line_signal and _last_seen in ("left_outer", "right_outer"))):
        action = "slow_down"
    elif no_line_signal:
        action = "straight"
    else:
        # Other patterns have not been calibrated for this sensor spacing.
        action = "stop_and_check"

    return {
        "action": action,
        "straight_signal": action == "straight",
        "adjust_left_signal": action == "adjust_left",
        "adjust_right_signal": action == "adjust_right",
        "slow_down_signal": action == "slow_down",
        "stop_signal": action == "stop_and_check",
        "left_turn_signal": bool(left_turn_signal),
        "right_turn_signal": bool(right_turn_signal),
        # Legacy name: 1111 alone cannot distinguish T/cross/wide markings.
        "t_junction_signal": bool(t_junction_signal),
        "no_line_signal": no_line_signal,
        "search_left_signal": search_left_signal,
        "search_right_signal": search_right_signal,
        "suspected_lost_signal": search_left_signal or search_right_signal,
        "zero_count": _zero_count,
        "last_seen": _last_seen,
    }
