from utime import sleep, ticks_ms, ticks_diff
import config
import servo

def turn_left_90(turn_min=1300, turn_max = 4000,
                 left_inverted=False, right_inverted=False):
    config.left_motor.Forward(50)
    config.right_motor.Forward(50)
    sleep(1.7)
    config.right_motor.Forward(50)
    config.left_motor.Reverse(50)
    start = ticks_ms()
    line_detected_since = None
    while True:
        elapsed = ticks_diff(ticks_ms(), start)
        if elapsed > turn_max:
            stop()
            break
        elif elapsed > turn_min:
            if config.middle_left_sensor.value() and config.middle_right_sensor.value():
                if line_detected_since is None:
                    line_detected_since = ticks_ms()
                elif ticks_diff(ticks_ms(), line_detected_since) >= 125:
                    config.right_motor.off()
                    config.left_motor.off()
                    return
            else:
                line_detected_since = None
                config.left_motor.Reverse(50)
                config.right_motor.Forward(50)



def turn_right_90(turn_min=1300, turn_max = 4000,
                 left_inverted=False, right_inverted=False):
    config.left_motor.Forward(50)
    config.right_motor.Forward(50)
    sleep(1.7)
    config.right_motor.Reverse(50)
    config.left_motor.Forward(50)
    start = ticks_ms()
    line_detected_since = None
    while True:
        elapsed = ticks_diff(ticks_ms(), start)
        if elapsed > turn_max:
            stop()
            break
        elif elapsed > turn_min:
            if config.middle_left_sensor.value() and config.middle_right_sensor.value():
                if line_detected_since is None:
                    line_detected_since = ticks_ms()
                elif ticks_diff(ticks_ms(), line_detected_since) >= 125:
                    config.right_motor.off()
                    config.left_motor.off()
                    return
            else:
                line_detected_since = None
                config.left_motor.Forward(50)
                config.right_motor.Reverse(50)

def turn_180(turn_min=4000, turn_max = 4500,
                 left_inverted=False, right_inverted=False):
    config.left_motor.off()
    config.right_motor.off()
    dropoff()
    sleep(2)


    config.left_motor.Reverse(50)
    config.right_motor.Reverse(50)
    sleep(1.5)
    config.right_motor.Reverse(50)
    config.left_motor.Forward(50)
    start = ticks_ms()
    overlap_timer = None
    while True:
        elapsed = ticks_diff(ticks_ms(), start)
        if elapsed > turn_max:
            stop()
            break
        elif elapsed > turn_min:
            if config.middle_left_sensor.value() and config.middle_right_sensor.value():
                if overlap_timer is None:
                    overlap_timer = ticks_ms()
                
                elif ticks_diff(ticks_ms(), overlap_timer) >= 100:
                    config.right_motor.off()
                    config.left_motor.off()
                    return
            else:
                overlap_timer = None
                config.left_motor.Forward(50)
                config.right_motor.Reverse(50)

def short_turn_180(turn_min=2500, turn_max = 4000,
                 left_inverted=False, right_inverted=False):
    config.right_motor.Forward(50)
    config.left_motor.Forward(50)
    sleep(0.5)
    config.right_motor.Reverse(50)
    config.left_motor.Forward(50)
    start = ticks_ms()
    overlap_timer = None
    while True:
        elapsed = ticks_diff(ticks_ms(), start)
        if elapsed > turn_max:
            stop()
            break
        elif elapsed > turn_min:
            if config.middle_left_sensor.value() and config.middle_right_sensor.value():
                if overlap_timer is None:
                    overlap_timer = ticks_ms()
                
                elif ticks_diff(ticks_ms(), overlap_timer) >= 130:
                    config.right_motor.off()
                    config.left_motor.off()
                    return
            else:
                overlap_timer = None
                config.left_motor.Forward(50)
                config.right_motor.Reverse(50)

def tight_turn_right_90(turn_min=1300, turn_max = 2500,
                 left_inverted=False, right_inverted=False):
    config.left_motor.Forward(50)
    config.right_motor.Forward(50)
    sleep(1.6)
    config.right_motor.Reverse(50)
    config.left_motor.Forward(50)
    start = ticks_ms()
    line_detected_since = None
    while True:
        elapsed = ticks_diff(ticks_ms(), start)
        if elapsed > turn_max:
            stop()
            break
        elif elapsed > turn_min:
            if config.middle_left_sensor.value() and config.middle_right_sensor.value():
                if line_detected_since is None:
                    line_detected_since = ticks_ms()
                elif ticks_diff(ticks_ms(), line_detected_since) >= 130:
                    config.right_motor.off()
                    config.left_motor.off()
                    stop()
                    return
            else:
                line_detected_since = None
                config.left_motor.Forward(50)
                config.right_motor.Reverse(50)


def tight_turn_left_90(turn_min=1300, turn_max = 2500,
                 left_inverted=False, right_inverted=False):
    config.left_motor.Forward(50)
    config.right_motor.Forward(50)
    sleep(1.6)
    config.right_motor.Forward(50)
    config.left_motor.Reverse(50)
    start = ticks_ms()
    line_detected_since = None
    while True:
        elapsed = ticks_diff(ticks_ms(), start)
        if elapsed > turn_max:
            stop()
            break
        elif elapsed > turn_min:
            if config.middle_left_sensor.value() and config.middle_right_sensor.value():
                if line_detected_since is None:
                    line_detected_since = ticks_ms()
                elif ticks_diff(ticks_ms(), line_detected_since) >= 140:
                    config.right_motor.off()
                    config.left_motor.off()
                    config.right_motor.Reverse(50)
                    config.left_motor.Reverse(50)
                    sleep(1.0)
                    stop()
                    return
            else:
                line_detected_since = None
                config.left_motor.Reverse(50)
                config.right_motor.Forward(50)

def pickup():
    stop()
    servo.servo1.set_angle(65)
    sleep(2)
    servo.servo2.set_angle(0)
    forward(50)
    sleep(1)
    stop()
    servo.servo1.set_angle(17.5)
    sleep(2)
    servo.servo2.set_angle(55)
    sleep(2)


def dropoff():
    stop()
    sleep(2)
    forward(50)
    sleep(0.3)
    stop()
    sleep(2)
    servo.servo1.set_angle(65)

def left_tap(
             left_inverted=False, right_inverted=False): 
    config.left_motor.Forward(40)
    config.right_motor.Forward(80)


def right_tap(left_inverted=False, right_inverted=False):
    config.left_motor.Forward(80)
    config.right_motor.Forward(40)


def forward(speed=80):
    config.left_motor.Forward(speed)
    config.right_motor.Forward(speed)

def reverse(speed=80):
    config.left_motor.Reverse(speed)
    config.right_motor.Reverse(speed)


def stop():
   config.left_motor.off()
   config.right_motor.off()
