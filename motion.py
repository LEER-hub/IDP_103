from utime import sleep


def turn_left_90(left_motor, right_motor, turn_time, speed=30,
                 left_inverted=False, right_inverted=False):
    """Pivot left using a duration calibrated for 90 degrees.

    Pass Motor objects in physical left/right order. turn_time is in seconds
    and must be measured on the robot at the selected speed (PWM percent).
    Set a motor's inverted flag if its Forward() makes that wheel go backward.
    This is a timed turn, not a measured angle; battery, load and surface
    changes can affect the result. Importing this module does not move motors.
    """
    if not 0 < turn_time < float("inf"):
        raise ValueError("turn_time must be a finite positive number of seconds")
    if not 0 < speed <= 100:
        raise ValueError("speed must be greater than 0 and at most 100")

    try:
        left_motor.off()
        right_motor.off()
        sleep(0.1)  # Brief pause before changing wheel directions.

        # A left pivot needs the left wheel backward and right wheel forward.
        if left_inverted:
            left_motor.Forward(speed)
        else:
            left_motor.Reverse(speed)

        if right_inverted:
            right_motor.Reverse(speed)
        else:
            right_motor.Forward(speed)

        sleep(turn_time)
    finally:
        # Also stop if the turn is interrupted or a motor command fails.
        try:
            left_motor.off()
        finally:
            right_motor.off()


def turn_right_90(left_motor, right_motor, turn_time, speed=30,
                  left_inverted=False, right_inverted=False):
    """Pivot right using a duration calibrated for 90 degrees.

    Arguments use the same physical left/right order as turn_left_90.
    Calibrate turn_time for right turns; it may differ from the left-turn time.
    """
    # Swap wheels and their flags to reuse validation and guaranteed cleanup:
    # the physical left wheel goes forward and the right wheel backward.
    turn_left_90(right_motor, left_motor, turn_time, speed,
                 left_inverted=right_inverted,
                 right_inverted=left_inverted)
