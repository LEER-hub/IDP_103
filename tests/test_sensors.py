"""Manual Pico sensor check; no motors are controlled by this script.

Keep sensors.py at the Pico filesystem root. Run this file from Thonny.
Fill SENSOR_PINS after wiring; use GP numbers, not physical pin numbers.
This script does not stop a previously running motor program: stop that
program and ensure the wheels are stopped before testing the sensors.
"""

from sensors import LineSensors
from utime import sleep


# Replace None with four actual GP numbers in this order:
# (left_outer, left_inner, right_inner, right_outer)
SENSOR_PINS = None
WHITE_LEVEL = 1  # Verify on white; interface circuitry may invert the signal.


def test_sensors(pins, white_level=WHITE_LEVEL):
    sensors = LineSensors(pins, white_level=white_level)
    print("Order: left_outer, left_inner, right_inner, right_outer")
    print("Move each sensor over white and dark surfaces. Ctrl+C to stop.")
    try:
        while True:
            raw = sensors.read_raw()
            # Derive the labels from the same sample as the printed raw values.
            labels = tuple("white" if value == white_level else "dark"
                           for value in raw)
            print("raw:", raw, "surface:", labels)
            sleep(0.1)
    except KeyboardInterrupt:
        print("Sensor test stopped")


if __name__ == "__main__":
    if SENSOR_PINS is None:
        print("Set SENSOR_PINS to your four GP numbers before running this test.")
    else:
        test_sensors(SENSOR_PINS)
