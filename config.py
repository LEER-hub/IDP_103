from machine import Pin, PWM, ADC
from motors import Motor

left_motor = Motor(dirPin=4, PWMPin=5)

right_motor = Motor(dirPin=7, PWMPin=6)

far_left_sensor = Pin(10, Pin.IN, Pin.PULL_UP)
middle_left_sensor = Pin(11, Pin.IN, Pin.PULL_UP)
middle_right_sensor = Pin(12, Pin.IN, Pin.PULL_UP)
far_right_sensor = Pin(13, Pin.IN, Pin.PULL_UP)

hall_sensor = ADC(26)
