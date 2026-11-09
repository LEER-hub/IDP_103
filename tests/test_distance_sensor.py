from machine import Pin, I2C
from utime import sleep
from libs.VL53L0X.VL53L0X import VL53L0X


def test_distance_sensor(holding_block=False):
    if holding_block:
        print("Claw is holding a block; skip distance detection.")
        return
    i2c = I2C(0, sda=Pin(16), scl=Pin(17))

    sensor = VL53L0X(i2c)

    try:
        sensor.start()

        while True:
            distance = sensor.read()
            print("Distance:", distance, "mm")
            if distance <= 0 or distance >= 8190:
                 return "INVALID"
            elif distance < 100:
                 return "FULL"
            else:
                 return "EMPTY"



    finally:
        sensor.stop()


if __name__ == "__main__":
    test_distance_sensor()
