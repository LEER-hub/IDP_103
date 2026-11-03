from machine import ADC, Pin
from time import sleep

hall = ADC(26)  # GP26 / ADC0
north_pin = Pin(20, Pin.OUT)
south_pin = Pin(19, Pin.OUT)
amber_led = Pin(21)


while True:
    value = hall.read_u16()
    voltage = value * 3.3 / 65535
    polarity = None

    if voltage < 1.80:
        print("South Pole")
        polarity = "south"
        south_pin.value(1)
        north_pin.value(0)

    elif voltage > 2.20:
        print("North Pole")
        polairty = "north"
        north_pin.value(1)
        south_pin.value(0)

    else:
        print("No magnet detected")
        north_pin.value(0)
        south_pin.value(0)

    print("ADC:", value, "| Voltage:", round(voltage, 3), "V")
    # amber_led.toggle()
    sleep(0.4)
