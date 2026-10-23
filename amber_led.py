from machine import Pin
from time import sleep

amber_led = Pin(19, Pin.OUT)

while True:
    amber_led.toggle()
    sleep(0.4)
