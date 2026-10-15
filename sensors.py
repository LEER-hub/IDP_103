from machine import Pin


class LineSensors:
    """Four digital line sensors in physical left-to-right order.

    pins: GP numbers, NOT connector/physical pin numbers, ordered as
    (left_outer, left_inner, right_inner, right_outer).
    white_level: measured digital level on white (0 or 1).
    The manual specifies 1, but verify after wiring and interface circuitry.
    """

    def __init__(self, pins, white_level=1):
        if len(pins) != 4:
            raise ValueError("Provide exactly four GP numbers, left to right")
        if any(type(number) is not int or number < 0 for number in pins):
            raise ValueError("GP numbers must be non-negative integers")
        if len(set(pins)) != 4:
            raise ValueError("Each sensor needs a different GP number")
        if white_level not in (0, 1):
            raise ValueError("white_level must be 0 or 1")

        self.pins = tuple(Pin(number, Pin.IN) for number in pins)
        self.white_level = white_level

    def read_raw(self):
        """Return four electrical readings (0/1), left to right."""
        return tuple(pin.value() for pin in self.pins)

    def read_white(self):
        """Return four booleans: True means white detected, left to right."""
        return tuple(value == self.white_level for value in self.read_raw())
