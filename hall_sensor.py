from machine import ADC, Pin
from time import sleep

hall = ADC(26)  # GP26 / ADC0
north_pin = Pin(21, Pin.OUT)
south_pin = Pin(20, Pin.OUT)
amber_led = Pin(19, Pin.OUT)


while True:
    value = hall.read_u16()
    voltage = value * 3.3 / 65535

    if voltage < 1.74:
        print("South Pole")
        south_pin.value(1)
        north_pin.value(0)

    elif voltage > 2.24:
        print("North Pole")
        north_pin.value(1)
        south_pin.value(0)

    else:
        print("No magnet detected")
        north_pin.value(0)
        south_pin.value(0)

    print("ADC:", value, "| Voltage:", round(voltage, 3), "V")
    amber_led.toggle()
    sleep(0.4)
