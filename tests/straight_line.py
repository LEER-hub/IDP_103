from motors import Motor
from utime import sleep

'''
pseudocode for straight line test:
1. motors will be positioned in a straight line
2. detection logic: 
a)all four trigger line = crossroad
b)only left two trigger lines = left turn
c)only right two trigger lines = right turn
d) if only one of the inner trigger lines is triggered, then the robot is off track and needs to be corrected

'''
