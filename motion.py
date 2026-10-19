from utime import sleep
import config

def turn_left_90(turn_time=1.54,
                 left_inverted=False, right_inverted=False):
    config.left_motor.Forward(50)
    config.right_motor.Forward(50)
    sleep(1.5)
    config.left_motor.Reverse(50)
    config.right_motor.Forward(50)
    sleep(turn_time)
    config.right_motor.off()
    config.left_motor.off()


def turn_right_90(turn_time=1.54,
                  left_inverted=False, right_inverted=False):
    config.left_motor.Forward(50)
    config.right_motor.Forward(50)
    sleep(1.5)
    config.left_motor.Forward(50)
    config.right_motor.Reverse(50)
    sleep(turn_time)
    config.right_motor.off()
    config.left_motor.off()

def turn_180(turn_time=3.08, left_inverted=False, right_inverted=False):
    print("Turning 180 degrees")
    config.left_motor.Reverse(50)
    config.right_motor.Forward(50)
    sleep(turn_time)
    config.right_motor.off()
    config.left_motor.off()
    print("Turn complete")

def left_tap(
             left_inverted=False, right_inverted=False):
    config.left_motor.Forward(35)
    config.right_motor.Forward(50)


def right_tap(left_inverted=False, right_inverted=False):
    config.left_motor.Forward(50)
    config.right_motor.Forward(35)


def forward(speed=50):
    config.left_motor.Forward(speed)
    config.right_motor.Forward(speed)

def reverse(speed=30):
    config.left_motor.Reverse(speed)
    config.right_motor.Reverse(speed)


def stop():
   config.left_motor.off()
   config.right_motor.off()
