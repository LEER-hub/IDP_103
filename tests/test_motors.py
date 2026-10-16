import config
from motors import Motor
from utime import sleep

def test_motor3_and4():
    motorleft = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP4/5
    motorright = Motor(dirPin=7, PWMPin=6)
    try:
        while True:
            print("Forward")
            motorleft.Forward()
            motorright.Forward()
            sleep(1)
            print("Reverse")
            motorleft.Reverse()
            motorright.Reverse()
            sleep(1)
    except KeyboardInterrupt:
        print("keyboard interrupted")
    
    finally:
        motorleft.off()
        motorright.off()

