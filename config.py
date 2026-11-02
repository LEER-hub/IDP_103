from machine import Pin, PWM, ADC, I2C
from motors import Motor
from servo import Servo
from libs.VL53L0X.VL53L0X import VL53L0X

# Motors
left_motor = Motor(dirPin=4, PWMPin=5)
right_motor = Motor(dirPin=7, PWMPin=6)

# Line sensors
far_left_sensor = Pin(8, Pin.IN, Pin.PULL_UP)
middle_left_sensor = Pin(9, Pin.IN, Pin.PULL_UP)
middle_right_sensor = Pin(10, Pin.IN, Pin.PULL_UP)
far_right_sensor = Pin(11, Pin.IN, Pin.PULL_UP)

# Flashing amber LED
amber_led = Pin(21, Pin.OUT)

# Hall sensor
hall_sensor = ADC(26)

# North and south LED's
north_pin = Pin(20, Pin.OUT)
south_pin = Pin(19, Pin.OUT)

# on off switch
on_off_switch = Pin(12, Pin.IN)  # not pressed = 1, pressed = 0

# Distance sensor
'''

i2c_bus = I2C(id=0, sda=Pin(6), scl=Pin(7))
vl53l0 = VL53L0X(i2c_bus)
vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[0], 18)
vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[1], 14)
'''

servo1 = Servo(Pin(13))  # Connected to Servo 1
servo2 = Servo(Pin(15))  # Connected to Servo 2
