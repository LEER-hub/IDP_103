from machine import Pin, PWM
import time
from dropoff_config import NORTHPOLE_DROPOFF, SOUTHPOLE_DROPOFF


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

    # Convert a command angle (0..MAX_ANGLE) to duty.
    def set_angle(self, angle):
        # Clamp angle
        if angle < 0:
            angle = 0
        if angle > Servo.MAX_ANGLE:
            angle = Servo.MAX_ANGLE

        duty = int(Servo.MIN_DUTY + (angle / Servo.SERVO_RANGE) *
                   (Servo.MAX_DUTY - Servo.MIN_DUTY))
        self.servo.duty_u16(duty)


servo1 = Servo(Pin(13))  # Gripper
servo2 = Servo(Pin(15))  # Lift

def open_gripper():
    servo1.set_angle(65)


def pickup():
    import motion

    motion.stop()
    servo2.set_angle(0)
    motion.forward(50)
    time.sleep(1)
    motion.stop()
    servo1.set_angle(17.5)
    time.sleep(2)
    servo2.set_angle(55)
    time.sleep(2)





def dropoff():
    """Legacy release used by motion.turn_180(); not the calibrated rack sequence."""
    import motion

    motion.stop()
    time.sleep(2)
    motion.forward(50)
    time.sleep(0.3)
    motion.stop()
    time.sleep(2)
    servo1.set_angle(65)


# Existing route experiments are retained below. The public pole dropoff
# functions do NOT use them: main must confirm arrival at the shelf first.
# In particular, losing the line alone does not prove arrival at a shelf.
def _read_line_sensors():
    import config

    return (
        config.far_left_sensor.value(),
        config.middle_left_sensor.value(),
        config.middle_right_sensor.value(),
        config.far_right_sensor.value(),
    )


def _line_readings(sensors, line_value):
    return tuple(int(value == line_value) for value in sensors)


def _is_node_signal(sensors, line_value):
    from line_follower import line_follow_algorithms_fourline

    left_turn, right_turn, t_junction, _, _, _ = line_follow_algorithms_fourline(
        *_line_readings(sensors, line_value)
    )
    return left_turn or right_turn or t_junction


def _follow_line(motion, sensors, line_value):
    from line_follower import line_follow_algorithms_fourline

    _, _, _, too_left, too_right, _ = line_follow_algorithms_fourline(
        *_line_readings(sensors, line_value)
    )
    if too_left:
        motion.right_tap()
    elif too_right:
        motion.left_tap()
    else:
        motion.forward()


def _find_route(start, destination):
    from line_follower import nodes

    queue = [start]
    previous = {start: None}
    for current in queue:
        if current == destination:
            break
        for neighbour in nodes[current]:
            if neighbour not in previous:
                previous[neighbour] = current
                queue.append(neighbour)

    if destination not in previous:
        raise ValueError("No route from {} to {}".format(start, destination))

    route = []
    current = destination
    while current is not None:
        route.append(current)
        current = previous[current]
    route.reverse()
    return route


def _turn_toward(current_node, next_node, heading):
    import motion
    from line_follower import nodes

    compass = ("north", "east", "south", "west")
    desired_heading = nodes[current_node][next_node]
    turn = (compass.index(desired_heading) - compass.index(heading)) % 4
    if turn == 1:
        motion.turn_right_90()
    elif turn == 2:
        motion.short_turn_180()
    elif turn == 3:
        motion.turn_left_90()
    return desired_heading


def _wait_for_node(motion, line_value=0, timeout_ms=20000):
    from utime import sleep_ms, ticks_diff, ticks_ms

    started = ticks_ms()
    clear_since = None
    signal_since = None
    armed = False

    while ticks_diff(ticks_ms(), started) < timeout_ms:
        sensors = _read_line_sensors()
        if _is_node_signal(sensors, line_value):
            clear_since = None
            if armed:
                if signal_since is None:
                    signal_since = ticks_ms()
                elif ticks_diff(ticks_ms(), signal_since) >= 80:
                    return
        else:
            signal_since = None
            if clear_since is None:
                clear_since = ticks_ms()
            elif ticks_diff(ticks_ms(), clear_since) >= 100:
                armed = True
        _follow_line(motion, sensors, line_value)
        sleep_ms(20)

    raise TimeoutError("Timed out while following the route between nodes")


def _drive_white_line_to_end(motion, timeout_ms=20000):
    from utime import sleep_ms, ticks_diff, ticks_ms

    started = ticks_ms()
    no_line_since = None
    acquired_line = False

    while ticks_diff(ticks_ms(), started) < timeout_ms:
        sensors = _read_line_sensors()
        if any(value == 1 for value in sensors):
            acquired_line = True
            no_line_since = None
            _follow_line(motion, sensors, 1)
        elif not acquired_line:
            motion.forward(35)
        else:
            if no_line_since is None:
                no_line_since = ticks_ms()
            elif ticks_diff(ticks_ms(), no_line_since) >= 250:
                motion.stop()
                return
            motion.stop()
        sleep_ms(20)

    raise TimeoutError("Timed out before reaching the rack branch endpoint")


def _navigate_route(route, heading):
    import motion

    if len(route) < 2:
        motion.stop()
        return heading

    heading = _turn_toward(route[0], route[1], heading)
    index = 1

    while index < len(route):
        if index == len(route) - 1:
            motion.stop()
            return heading

        _wait_for_node(motion, line_value=0)
        current_node = route[index]
        next_node = route[index + 1]
        heading = _turn_toward(current_node, next_node, heading)
        if next_node[-1] in ("u", "l"):
            _drive_white_line_to_end(motion)
            return heading
        index += 1

    motion.stop()
    return heading


def _return_from_white_branch(route, heading):
    import motion

    acquired_line = False
    no_line_since = None
    from utime import sleep_ms, ticks_diff, ticks_ms

    started = ticks_ms()
    while ticks_diff(ticks_ms(), started) < 20000:
        sensors = _read_line_sensors()
        if any(value == 1 for value in sensors):
            acquired_line = True
            no_line_since = None
            _follow_line(motion, sensors, 1)
        elif acquired_line:
            if no_line_since is None:
                no_line_since = ticks_ms()
            elif ticks_diff(ticks_ms(), no_line_since) >= 250:
                motion.stop()
                break
            motion.stop()
        else:
            motion.forward(35)
        sleep_ms(20)
    else:
        raise TimeoutError("Timed out while reacquiring the white rack branch")

    reversed_route = list(reversed(route))
    if len(reversed_route) < 3:
        motion.stop()
        return

    current_node = reversed_route[1]
    next_node = reversed_route[2]
    heading = _turn_toward(current_node, next_node, heading)
    for index in range(2, len(reversed_route)):
        _wait_for_node(motion, line_value=0)
        if index == len(reversed_route) - 1:
            motion.stop()
            return
        heading = _turn_toward(
            reversed_route[index], reversed_route[index + 1], heading
        )


def _validated_dropoff_profile(profile):
    """Check every setting before moving; return a stable copy for this run."""
    angle_keys = (
        "insert_lift_angle", "release_lift_angle", "travel_lift_angle",
        "gripper_open_angle",
    )
    speed_keys = ("insert_speed", "retreat_speed")
    time_keys = (
        "insert_time_s", "retreat_time_s", "lift_settle_s",
        "gripper_open_wait_s",
    )
    keys = angle_keys + speed_keys + time_keys
    missing = [key for key in keys if profile.get(key) is None]
    if missing:
        raise ValueError(
            "TODO CALIBRATE in dropoff_config.py: " + ", ".join(missing)
        )

    checked = {}
    for key in keys:
        value = profile[key]
        if (isinstance(value, bool) or not isinstance(value, (int, float))
                or not -float("inf") < value < float("inf")):
            raise ValueError(key + " must be a finite number")
        if key in angle_keys:
            if not 0 <= value <= Servo.MAX_ANGLE:
                raise ValueError(
                    key + " must be between 0 and " + str(Servo.MAX_ANGLE)
                )
        elif key in speed_keys:
            if not 0 < value <= 100:
                raise ValueError(key + " must be greater than 0 and at most 100")
        elif value <= 0:
            raise ValueError(key + " must be greater than 0 seconds")
        checked[key] = value
    return checked


def _dropoff_at(target_node, allowed_suffix, profile, at_rack=False):
    """Place a held block from an already aligned, stopped shelf approach pose.

    This is a placement sequence, not navigation. Keep gripping the block
    until the shelf takes its weight. Reverse clear before changing the lift
    to travel height. On failure, stop wheels without guessing a recovery
    gripper/lift movement. No turn or return-to-start movement happens here.
    """

    import motion

    try:
        motion.stop()
        if not isinstance(target_node, str):
            raise ValueError("Target node must be a string such as 'a3u' or 'b2l'")
        target_node = target_node.strip().lower()
        if (len(target_node) != 3 or target_node[0] not in ("a", "b")
                or target_node[1] not in "123456"
                or target_node[2] != allowed_suffix):
            raise ValueError(
                "Target must be an A/B rack node ending in " + allowed_suffix
            )
        if at_rack is not True:
            raise ValueError(
                "Navigate to the target shelf and stop aligned first; "
                "then call with at_rack=True. This function does not navigate."
            )
        settings = _validated_dropoff_profile(profile)

        # 1. Still holding the block, lift to the insertion height.
        servo2.set_angle(settings["insert_lift_angle"])
        time.sleep(settings["lift_settle_s"])

        # 2. Push the held block into the rack, then stop before releasing.
        motion.forward(settings["insert_speed"])
        time.sleep(settings["insert_time_s"])
        motion.stop()

        # 3. Transfer the load onto the shelf before opening the gripper.
        servo2.set_angle(settings["release_lift_angle"])
        time.sleep(settings["lift_settle_s"])
        servo1.set_angle(settings["gripper_open_angle"])
        time.sleep(settings["gripper_open_wait_s"])

        # 4. Keep the gripper open and at release height until fully clear.
        motion.reverse(settings["retreat_speed"])
        time.sleep(settings["retreat_time_s"])
        motion.stop()

        # 5. Only now move the empty lift to its travel position.
        servo2.set_angle(settings["travel_lift_angle"])
        time.sleep(settings["lift_settle_s"])
    finally:
        motion.stop()

    # No placement sensor is available: this reports execution, not proof
    # that the block is in the rack. main can resume navigation from here.
    return {
        "target_node": target_node,
        "pole": "north" if allowed_suffix == "u" else "south",
        "sequence_complete": True,
        "placement_confirmed": False,
    }


def northpole_dropoff(target_node, at_rack=False):
    """Place a north-pole block at an already reached U-side rack target."""
    return _dropoff_at(target_node, "u", NORTHPOLE_DROPOFF, at_rack)


def southpole_dropoff(target_node, at_rack=False):
    """Place a south-pole block at an already reached L-side rack target."""
    return _dropoff_at(target_node, "l", SOUTHPOLE_DROPOFF, at_rack)


def southpole(target_node, at_rack=False):
    """Compatibility alias for southpole_dropoff."""
    return southpole_dropoff(target_node, at_rack=at_rack)


def north_pole_dropoff(target_node, at_rack=False):
    """Compatibility alias for northpole_dropoff."""
    return northpole_dropoff(target_node, at_rack=at_rack)


def south_pole_dropoff(target_node, at_rack=False):
    """Compatibility alias for southpole_dropoff."""
    return southpole_dropoff(target_node, at_rack=at_rack)
