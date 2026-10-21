import config
from motion import turn_left_90, turn_right_90, turn_180, left_tap, right_tap, forward, reverse, stop
from utime import sleep
import motion
motion.stop()
print("Starting test_turns.py")
sleep(3)
try:
    while True:
        print("Turning left 90 degrees")
        turn_left_90()
        sleep(3)
        print("Turning right 90 degrees")
        turn_right_90()
        sleep(3)
        print("Turning 180 degrees")
        turn_180()
        sleep(3)
        print("Left tap")
        left_tap()
        sleep(3)
        print("Right tap")
        right_tap()
        sleep(3)
        print("Forward")
        forward()
        sleep(3)
        print("Reverse")
        reverse()
        sleep(3)
except KeyboardInterrupt:
         print("keyboard interrupted")
finally:
      stop()