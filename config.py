from machine import Pin, PWM, ADC, I2C
from motors import Motor

left_motor = Motor(dirPin=4, PWMPin=5)

right_motor = Motor(dirPin=7, PWMPin=6)

far_left_sensor = Pin(10, Pin.IN, Pin.PULL_UP)
middle_left_sensor = Pin(11, Pin.IN, Pin.PULL_UP)
middle_right_sensor = Pin(12, Pin.IN, Pin.PULL_UP)
far_right_sensor = Pin(13, Pin.IN, Pin.PULL_UP)

hall_sensor = ADC(26)

# Distance sensor (VL53L0X, I2C0 on GP8 SDA / GP9 SCL)
tof = VL53L0X(i2c_bus)
tof.set_Vcsel_pulse_period(
    tof.vcsel_period_type[0], 18)  # optional: long range
tof.set_Vcsel_pulse_period(
    tof.vcsel_period_type[1], 14)  # optional: long range
tof.start()


def get_distance():
    """Returns distance in mm, or None if no reading / nothing in range."""
    try:
        d = tof.read()
    except OSError:  # includes TimeoutError
        return None
    if d is None or d > 8000:
        return None
    return d
