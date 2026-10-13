from motors import Motor
from utime import sleep

def test_motor3_and4():
    motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP4/5
    motor4 = Motor(dirPin=7, PWMPin=6)
    try:
        while True:
            print("Forward")
            motor3.Forward()
            motor4.Forward()
            sleep(1)
            print("Reverse")
            motor3.Reverse()
            motor4.Reverse()
            sleep(1)
    except KeyboardInterrupt:
        print("keyboard interrupted")
    
    finally:
        motor3.off()
        motor4.off()


if __name__ == "__main__":
    test_motor3_and4()