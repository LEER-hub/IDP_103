# North- and south-pole shelf dropoff

`servo1` is the gripper and `servo2` is the lift. The functions use the
existing routing convention: north-pole packages go to U-side rack nodes
(`a1u`..`a6u`, `b1u`..`b6u`); south-pole packages go to L-side nodes
(`a1l`..`a6l`, `b1l`..`b6l`). The caller selects the pole and target; these
functions do not read the Hall sensor.

## Starting and finishing positions

**Before calling:** the robot must already be stopped, facing the correct
shelf, holding the package, at the same stand-off position used for
calibration. The lift must be able to move at that position. `at_rack=True`
is the caller's explicit confirmation of that state, not a sensor reading.

**Sequence:** stop wheels; set insertion height; wait; insert the held
package slowly; stop; move the lift until the shelf supports the package;
wait; open the gripper fully; wait; reverse straight out; stop; move the
empty lift to travel height; wait; leave wheels stopped.

The gripper remains open after the sequence. The robot still faces the
shelf and has reversed by the calibrated retreat amount. It does not turn
around, return to C0, or automatically update the navigation node/heading.
The navigation code must account for this finishing position.

On an exception or keyboard interrupt, the wheels stop. The function does
not guess whether it should open, close, lower, or reverse after a failure.

## Fill the marked parameters first

Edit `NORTHPOLE_DROPOFF` and `SOUTHPOLE_DROPOFF` in `dropoff_config.py`.
Every `None` has a `TODO CALIBRATE` comment. All settings are checked before
the first servo movement or driving command. Missing settings raise an
error listing their names.

| Parameter | Meaning / how to calibrate |
| --- | --- |
| `insert_lift_angle` | Lift command that lets the held package clear the shelf lip. |
| `release_lift_angle` | Lift command at which the shelf supports the package before the gripper opens. |
| `travel_lift_angle` | Empty lift position for travel, applied only after reversing clear. |
| `insert_speed` | Forward PWM percentage for the insertion. |
| `insert_time_s` | Time to insert from the agreed starting position, at that speed. |
| `retreat_speed` | Reverse PWM percentage for withdrawal. |
| `retreat_time_s` | Time needed to clear the shelf with the gripper fully open. |
| `lift_settle_s` | Wait after each lift movement, long enough for the slowest of the three movements. |
| `gripper_open_angle` | Existing value `65` from `open_gripper()`; verify full opening on the mechanism. |
| `gripper_open_wait_s` | Time to let the gripper open before withdrawal. |

Angles are servo commands, not heights in millimetres. The existing
`SERVO_RANGE = 90`, pulse limits and `MAX_ANGLE = 80` have been preserved;
check that mapping against the actual servo/linkage. Lowering the lift can
require either a smaller or a larger angle. The release angle may equal
the insertion angle if the shelf already carries the load there.

Calibrate the two profiles separately. The profiles assume a repeatable
approach position at each bay. If bays differ, calibrate and select the
appropriate profile before calling. Start with the lift/gripper positions,
then establish slow insertion and withdrawal settings. Confirm full
withdrawal before testing the travel-height movement.

This version uses timed driving because there is no confirmed insertion
distance sensor/encoder interface. Timing is not a measurement of depth,
and it cannot detect obstructions. Test under the actual load and battery
conditions; do not fill arbitrary angles or times just to remove the error.

## Calling from main

Call exactly one branch after your navigation code confirms the shelf
approach position. Substitute your actual target, for example:

```python
from servo import northpole_dropoff, southpole_dropoff

# Example: ONLY after arrival, alignment and calibration.
result = northpole_dropoff("a3u", at_rack=True)

# For a south-pole package, use this instead:
# result = southpole_dropoff("b2l", at_rack=True)
```

`north_pole_dropoff`, `south_pole_dropoff`, and the old name `southpole`
are aliases. All require `at_rack=True`. An old call containing only a
target now gives a clear error rather than assuming it may navigate or
insert from the current position.

The returned dictionary contains `target_node`, `pole`,
`sequence_complete=True`, and `placement_confirmed=False`. Completion
means the commands and waits ran; there is no sensor confirmation that
the package was successfully deposited.

## Existing main / motion integration

The current `main.py` opens the gripper at startup. It still calls `motion.turn_180()`,
which calls the old `dropoff()` internally and then reverses and turns.
Therefore uploading these functions alone does **not** switch main to
the new north/south sequence.

At the shelf, replace that old combined operation in your main workflow
with the selected pole dropoff, followed by a separately tested turn and
navigation step from the new finishing position. Do **not** immediately
call `motion.turn_180()` after a pole dropoff: it would attempt another
release and retreat. `short_turn_180()` also moves forward before pivoting;
it is not a pure in-place turn and needs its own clearance check.

The old private routing experiments in `servo.py` are retained, but the
new public dropoff functions do not call them. Their line-loss endpoint
detection and line-polarity assumptions still need separate work before
automatic travel to/from a shelf can be relied on.

## Desktop verification

From the repository folder on the computer:

```powershell
python tests/test_dropoff_logic.py
```

This test uses fake motors, servos and time. It does not connect to a Pico,
run the robot, or prove mechanical calibration. Do not run it as the robot's
hardware test script.
