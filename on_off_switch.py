from machine import Pin
from time import sleep, sleep_ms
import motion


on_off_switch = Pin(18, Pin.IN)  # not pressed = 1, pressed = 0
amber_led = Pin(19, Pin.OUT)

motion.stop()
amber_led.value(0)
running = False
last_state = 1  # initially unpressed

while True:
    state = on_off_switch.value()
    if state == 0 and last_state == 1:
        running = not running
        motion.stop()
        if running:
            print("ON")
            motion.forward()
        else:
            print("OFF")
            motion.stop()
        sleep_ms(200)  # debounce

    last_state = state
    sleep_ms(10)
