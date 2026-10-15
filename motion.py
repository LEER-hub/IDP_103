from utime import sleep
import config

def turn_left_90(turn_time=2,
                 left_inverted=False, right_inverted=False):
    config.left_motor.Reverse(50)
    config.right_motor.Forward(50)
    sleep(turn_time)
    config.right_motor.off()
    config.left_motor.off()


def turn_right_90(turn_time=2,
                  left_inverted=False, right_inverted=False):
    config.left_motor.Forward(50)
    config.right_motor.Reverse(50)
    sleep(turn_time)
    config.right_motor.off()
    config.left_motor.off()

def left_tap(turn_time = 0.5,
             left_inverted=False, right_inverted=False):
    config.left_motor.Forward(40)
    config.right_motor.Forward(50)
    sleep(turn_time)


def right_tap(turn_time = 0.5,
              left_inverted=False, right_inverted=False):
    config.left_motor.Forward(50)
    config.right_motor.Forward(40)
    sleep(turn_time)
    config.right_motor.off()
    config.left_motor.off()


def forward(speed=50):
    config.left_motor.Forward(speed)
    config.right_motor.Forward(speed)

def reverse(speed=50):
    config.left_motor.Reverse(speed)
    config.right_motor.Reverse(speed)


def stop():
    """Stop both motors."""
    try:
        config.left_motor.off()
    finally:
        config.right_motor.off()
