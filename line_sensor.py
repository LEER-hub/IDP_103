from machine import Pin
from time import sleep

# GP15 is connected to the line sensor's OUT pin
line_sensor = Pin(11, Pin.IN, Pin.PULL_UP)

while True:
    value = line_sensor.value()

    if value == 0:
        print("BLACK")
    else:
        print("WHITE")

    sleep(0.2)
