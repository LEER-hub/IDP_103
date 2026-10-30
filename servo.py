from machine import Pin, PWM
import time


class Servo:
    # 50 Hz (20 ms period)
    # 0.5 ms pulse → 0°, 2.5 ms pulse → SERVO_RANGE
    # Pico 16-bit duty: 0.025 * 65535 = 1638, 0.125 * 65535 = 8192
    MIN_DUTY = 1638    # 0.5 ms (0°)
    MAX_DUTY = 8192    # 2.5 ms (full travel)
    # physical travel of the servo (change to 270 if needed)
    SERVO_RANGE = 150
    MAX_ANGLE = 150     # limit we allow

    def __init__(self, ServoPin):
        self.servo = PWM(ServoPin)
        self.servo.freq(50)  # 50 Hz for servo

    # Convert angle (0–30) to duty
    def set_angle(self, angle):
        # Clamp angle
        if angle < 0:
            angle = 0
        if angle > Servo.MAX_ANGLE:
            angle = Servo.MAX_ANGLE

        duty = int(Servo.MIN_DUTY + (angle / Servo.SERVO_RANGE) *
                   (Servo.MAX_DUTY - Servo.MIN_DUTY))
        self.servo.duty_u16(duty)


# dropoff()
