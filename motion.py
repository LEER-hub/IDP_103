from utime import sleep
import config

def turn_left_90(turn_time=0.73,
                 left_inverted=False, right_inverted=False):
    config.left_motor.Forward()
    config.right_motor.Forward()
    sleep(0.65)
    config.left_motor.Reverse()
    config.right_motor.Forward()
    sleep(turn_time)
    config.right_motor.off()
    config.left_motor.off()


def turn_right_90(turn_time=0.73,
                  left_inverted=False, right_inverted=False):
    config.left_motor.Forward()
    config.right_motor.Forward()
    sleep(0.65)
    config.left_motor.Forward()
    config.right_motor.Reverse()
    sleep(turn_time)
    config.right_motor.off()
    config.left_motor.off()

def turn_180(turn_time=1.46, left_inverted=False, right_inverted=False):
    print("Turning 180 degrees")
    config.left_motor.Reverse()
    config.right_motor.Forward()
    sleep(turn_time)
    config.right_motor.off()
    config.left_motor.off()
    print("Turn complete")

def left_tap(
             left_inverted=False, right_inverted=False):
    config.left_motor.Forward(60)
    config.right_motor.Forward(80)


def right_tap(left_inverted=False, right_inverted=False):
    config.left_motor.Forward(80)
    config.right_motor.Forward(60)


def forward(speed=80):
    config.left_motor.Forward(speed)
    config.right_motor.Forward(speed)

def reverse(speed=80):
    config.left_motor.Reverse(speed)
    config.right_motor.Reverse(speed)


def stop():
   config.left_motor.off()
   config.right_motor.off()
