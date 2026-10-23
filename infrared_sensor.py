from machine import Pin
from time import sleep_ms

ir = Pin(27, Pin.IN)

while True:
    if ir.value() == 0:        # LOW = burst of carrier detected
        print("IR signal!")
    sleep_ms(20)
