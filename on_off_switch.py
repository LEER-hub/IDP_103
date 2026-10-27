from machine import Pin
from time import sleep, sleep_ms
import motion


on_off_switch = Pin(12, Pin.IN)  # not pressed = 1, pressed = 0

motion.stop()
running = False
last_state = 1  # initially unpressed

while True:
    state = on_off_switch.value()
    if state == 0 and last_state == 1:
        running = not running
        motion.stop()
        if running:
            print("ON")

        else:
            print("OFF")
            motion.stop()
        sleep_ms(200)  # debounce

    last_state = state
    sleep_ms(10)
