from machine import Pin, PWM
import time
import motion


class Servo:
    # 50 Hz (20 ms period)
    # 0.5 ms pulse → 0°, 2.5 ms pulse → SERVO_RANGE
    # Pico 16-bit duty: 0.025 * 65535 = 1638, 0.125 * 65535 = 8192
    MIN_DUTY = 1638    # 0.5 ms (0°)
    MAX_DUTY = 8192    # 2.5 ms (full travel)
    SERVO_RANGE = 90   # physical travel of the servo (change to 270 if needed)
    MAX_ANGLE = 80     # limit we allow

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


# Test Code
servo1 = Servo(Pin(13))  # Connected to Servo 1
servo2 = Servo(Pin(15))  # Connected to Servo 2


def pickup():
    motion.stop()
    servo1.set_angle(65)
    time.sleep(2)
    servo2.set_angle(0)
    motion.forward(50)
    time.sleep(1)
    motion.stop()
    servo1.set_angle(17.5)
    time.sleep(2)
    servo2.set_angle(55)
    time.sleep(2)


def dropoff():
    motion.stop()
    time.sleep(2)
    motion.forward(50)
    time.sleep(0.3)
    motion.stop()
    time.sleep(2)
    servo1.set_angle(65)


# dropoff()
