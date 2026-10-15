from machine import ADC
from time import sleep

hall = ADC(26)  # GP26 / ADC0

while True:
    value = hall.read_u16()
    voltage = value * 3.3 / 65535

    if voltage < 1.7:
        print("South Pole")
    elif voltage > 2.3:
        print("North Pole")
    else:
        print("No magnet detected")

    print("ADC:", value, "| Voltage:", round(voltage, 3), "V")

    sleep(0.2)
