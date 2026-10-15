from utime import sleep
import config

def turn_left_90(turn_time, speed=70,
                 left_inverted=False, right_inverted=False):
    """Pivot left using a duration calibrated for 90 degrees.

    Uses the left and right motors from config. turn_time is in seconds
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
        config.left_motor.off()
        config.right_motor.off()
        sleep(0.1)  # Brief pause before changing wheel directions.

        # A left pivot needs the left wheel backward and right wheel forward.
        if left_inverted:
            config.left_motor.Forward(speed)
        else:
            config.left_motor.Reverse(speed)

        if right_inverted:
            config.right_motor.Reverse(speed)
        else:
            config.right_motor.Forward(speed)

        sleep(turn_time)
    finally:
        # Also stop if the turn is interrupted or a motor command fails.
        try:
            config.left_motor.off()
        finally:
            config.right_motor.off()


def turn_right_90(turn_time, speed=30,
                  left_inverted=False, right_inverted=False):
    """Pivot right using a duration calibrated for 90 degrees.

    Calibrate turn_time for right turns; it may differ from the left-turn time.
    """
    if not 0 < turn_time < float("inf"):
        raise ValueError("turn_time must be a finite positive number of seconds")
    if not 0 < speed <= 100:
        raise ValueError("speed must be greater than 0 and at most 100")

    try:
        config.left_motor.off()
        config.right_motor.off()
        sleep(0.1)

        if left_inverted:
            config.left_motor.Reverse(speed)
        else:
            config.left_motor.Forward(speed)

        if right_inverted:
            config.right_motor.Forward(speed)
        else:
            config.right_motor.Reverse(speed)

        sleep(turn_time)
    finally:
        try:
            config.left_motor.off()
        finally:
            config.right_motor.off()


def left_tap(turn_time = 0.5, speed=30,
             left_inverted=False, right_inverted=False):
    config.left_motor.Forward(40)
    config.right_motor.Forward(50)


def right_tap(turn_time = 0.5, speed=30,
              left_inverted=False, right_inverted=False):
    config.left_motor.Forward(50)
    config.right_motor.Forward(40)


def forward(speed=100):
    config.left_motor.Forward(speed)
    config.right_motor.Forward(speed)

def reverse(speed=100):
    config.left_motor.Reverse(speed)
    config.right_motor.Reverse(speed)


def stop():
    """Stop both motors."""
    try:
        config.left_motor.off()
    finally:
        config.right_motor.off()
