"""Shelf placement calibration. None means TODO CALIBRATE, never zero.

servo1 = gripper; servo2 = lift. Angles use servo.py's existing 0..80
command scale, NOT shelf heights in mm. Verify its pulse/angle mapping on
the actual mechanism before filling these values. North uses U-side rack
targets; south uses L-side rack targets, following the existing project map.

Use a repeatable stopped, aligned position in front of the shelf. Calibrate
insertion and retreat with the selected speeds, load and battery condition.
Timed driving cannot detect an obstruction or verify package placement.
"""


# NORTH: upper rack / U-side target, e.g. a3u or b2u.
NORTHPOLE_DROPOFF = {
    "insert_lift_angle": None,     # TODO CALIBRATE: clear the shelf lip while holding the block.
    "release_lift_angle": None,    # TODO CALIBRATE: shelf supports the block BEFORE opening.
    "travel_lift_angle": None,     # TODO CALIBRATE: empty gripper travel height after retreat.
    "insert_speed": None,          # TODO CALIBRATE: slow forward PWM percentage, 0 < value <= 100.
    "insert_time_s": None,         # TODO CALIBRATE: insertion time from the agreed starting pose.
    "retreat_speed": None,         # TODO CALIBRATE: slow reverse PWM percentage.
    "retreat_time_s": None,        # TODO CALIBRATE: reverse until the OPEN gripper clears the rack.
    "lift_settle_s": None,         # TODO CALIBRATE: wait long enough for each lift movement.
    "gripper_open_angle": 65,      # Existing open_gripper() value; verify fully open on the robot.
    "gripper_open_wait_s": None,   # TODO CALIBRATE: wait for the gripper to open before reversing.
}


# SOUTH: lower rack / L-side target, e.g. a3l or b2l.
# Calibrate separately; do not assume the same angle or travel time as north.
SOUTHPOLE_DROPOFF = {
    "insert_lift_angle": None,     # TODO CALIBRATE: lower rack insertion height.
    "release_lift_angle": None,    # TODO CALIBRATE: transfer the block's weight to the shelf.
    "travel_lift_angle": None,     # TODO CALIBRATE: empty gripper travel height after retreat.
    "insert_speed": None,          # TODO CALIBRATE: slow forward PWM percentage.
    "insert_time_s": None,         # TODO CALIBRATE: lower rack insertion duration.
    "retreat_speed": None,         # TODO CALIBRATE: slow reverse PWM percentage.
    "retreat_time_s": None,        # TODO CALIBRATE: full gripper clearance, not just insertion depth.
    "lift_settle_s": None,         # TODO CALIBRATE: settling time for each lift movement.
    "gripper_open_angle": 65,      # Existing open_gripper() value; verify on the robot.
    "gripper_open_wait_s": None,   # TODO CALIBRATE: opening time before retreat.
}

# Mechanical lowering may increase OR decrease the servo command angle.
# release_lift_angle can equal insert_lift_angle if the shelf already supports
# the block there. Determine this physically; do not assume an angle ordering.
