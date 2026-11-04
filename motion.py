from utime import sleep, ticks_ms, ticks_diff
import config


def turn_left_90(turn_min=1700, turn_max=4000,
                 left_inverted=False, right_inverted=False):
    config.left_motor.Forward(50)
    config.right_motor.Forward(50)
    sleep(1.75)
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
                elif ticks_diff(ticks_ms(), line_detected_since) >= 100:
                    config.right_motor.off()
                    config.left_motor.off()
                    return
            else:
                line_detected_since = None
                config.left_motor.Reverse(50)
                config.right_motor.Forward(50)


def turn_right_90(turn_min=1700, turn_max=4000,
                  left_inverted=False, right_inverted=False):
    config.left_motor.Forward(50)
    config.right_motor.Forward(50)
    sleep(1.75)
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
                elif ticks_diff(ticks_ms(), line_detected_since) >= 100:
                    config.right_motor.off()
                    config.left_motor.off()
                    return
            else:
                line_detected_since = None
                config.left_motor.Forward(50)
                config.right_motor.Reverse(50)


def turn_180(turn_min=4500, turn_max=5500,
             left_inverted=False, right_inverted=False):
    config.left_motor.off()
    config.right_motor.off()
    sleep(2)

    config.left_motor.Reverse(50)
    config.right_motor.Reverse(50)
    sleep(1.0)
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


def short_turn_180(turn_min=2500, turn_max=5000,
                   left_inverted=False, right_inverted=False):
    config.right_motor.Forward(50)
    config.left_motor.Forward(50)
    sleep(1.0)
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


def tight_turn_right_90(turn_min=1300, turn_max=2500,
                        left_inverted=False, right_inverted=False):
    config.left_motor.Forward(100)
    config.right_motor.Forward(100)
    sleep(0.8)
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


def tight_turn_left_90(turn_min=1300, turn_max=2500,
                       left_inverted=False, right_inverted=False):
    config.left_motor.Forward(100)
    config.right_motor.Forward(100)
    sleep(0.8)
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
    config.servo1.set_angle(132.5)
    sleep(0.5)
    config.servo2.set_angle(0)
    forward(50)
    sleep(0.8)
    stop()
    config.servo1.set_angle(37.5)
    sleep(0.5)
    config.servo2.set_angle(110)
    sleep(0.5)


def dropoff():
    stop()
    sleep(0.5)
    forward(50)
    sleep(0.3)
    stop()
    sleep(0.5)
    config.servo1.set_angle(70)


def left_tap(
        left_inverted=False, right_inverted=False):
    config.left_motor.Forward(50)
    config.right_motor.Forward(100)


def right_tap(left_inverted=False, right_inverted=False):
    config.left_motor.Forward(100)
    config.right_motor.Forward(50)


def forward(speed=100):
    config.left_motor.Forward(speed)
    config.right_motor.Forward(speed)


def reverse(speed=100):
    config.left_motor.Reverse(speed)
    config.right_motor.Reverse(speed)


def stop():
    config.left_motor.off()
    config.right_motor.off()


def amber_led_toggle():
    while True:
        config.amber_led.toggle()
        sleep(1)


def check_hall_sensor():    # logic from hall_sensor.py
    value = config.hall_sensor.read_u16()
    voltage = value * 3.3 / 65535
    polarity = None

    if voltage < 1.95:
        print("South Pole")
        polarity = "south"
        config.south_pin.value(1)
        config.north_pin.value(0)

    elif voltage > 1.95:
        print("North Pole")
        polarity = "north"
        config.north_pin.value(1)
        config.south_pin.value(0)

    else:
        print("No magnet detected")
        config.north_pin.value(0)
        config.south_pin.value(0)

    print("ADC:", value, "| Voltage:", round(voltage, 3), "V")
    sleep(0.4)
    return polarity
    # amber_led.toggle()


# pickup()
# dropoff()
