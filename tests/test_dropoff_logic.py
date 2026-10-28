"""Offline dropoff checks; run with desktop Python, never on the robot.

All hardware and timing modules are replaced before importing servo.py.
The numbers below are synthetic test inputs, NOT robot calibration values.
"""

import importlib
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]

NORTH_TEST_PROFILE = {
    "insert_lift_angle": 60,
    "release_lift_angle": 55,
    "travel_lift_angle": 10,
    "insert_speed": 30,
    "insert_time_s": 0.4,
    "retreat_speed": 25,
    "retreat_time_s": 0.8,
    "lift_settle_s": 1.2,
    "gripper_open_angle": 65,
    "gripper_open_wait_s": 0.6,
}

SOUTH_TEST_PROFILE = {
    "insert_lift_angle": 25,
    "release_lift_angle": 20,
    "travel_lift_angle": 12,
    "insert_speed": 24,
    "insert_time_s": 0.5,
    "retreat_speed": 22,
    "retreat_time_s": 0.9,
    "lift_settle_s": 1.1,
    "gripper_open_angle": 64,
    "gripper_open_wait_s": 0.7,
}


def expected_events(profile):
    return [
        ("stop",),
        ("lift", profile["insert_lift_angle"]),
        ("sleep", profile["lift_settle_s"]),
        ("forward", profile["insert_speed"]),
        ("sleep", profile["insert_time_s"]),
        ("stop",),
        ("lift", profile["release_lift_angle"]),
        ("sleep", profile["lift_settle_s"]),
        ("gripper", profile["gripper_open_angle"]),
        ("sleep", profile["gripper_open_wait_s"]),
        ("reverse", profile["retreat_speed"]),
        ("sleep", profile["retreat_time_s"]),
        ("stop",),
        ("lift", profile["travel_lift_angle"]),
        ("sleep", profile["lift_settle_s"]),
        ("stop",),
    ]


class DropoffLogicTests(unittest.TestCase):
    def setUp(self):
        self.events = []
        self.fail_at_call = None
        self.injected_error = RuntimeError("Injected hardware failure")
        self.pwm_writes = []

        fake_machine = types.ModuleType("machine")

        class FakePin:
            def __init__(self, number):
                self.number = number

        pwm_writes = self.pwm_writes

        class FakePWM:
            def __init__(self, pin):
                self.pin = pin

            def freq(self, value):
                pass

            def duty_u16(self, value):
                pwm_writes.append((self.pin.number, value))

        fake_machine.Pin = FakePin
        fake_machine.PWM = FakePWM
        fake_motion = types.ModuleType("motion")
        fake_motion.stop = lambda: self.record("stop")
        fake_motion.forward = lambda speed: self.record("forward", speed)
        fake_motion.reverse = lambda speed: self.record("reverse", speed)
        fake_time = types.ModuleType("time")
        fake_time.sleep = lambda seconds: self.record("sleep", seconds)
        fake_calibration = types.ModuleType("dropoff_config")
        fake_calibration.NORTHPOLE_DROPOFF = dict(NORTH_TEST_PROFILE)
        fake_calibration.SOUTHPOLE_DROPOFF = dict(SOUTH_TEST_PROFILE)
        self.calibration = fake_calibration

        self.module_patch = mock.patch.dict(sys.modules, {
            "machine": fake_machine,
            "motion": fake_motion,
            "time": fake_time,
            "dropoff_config": fake_calibration,
        })
        self.module_patch.start()
        self.addCleanup(self.module_patch.stop)

        spec = importlib.util.spec_from_file_location("servo", ROOT / "servo.py")
        self.servo = importlib.util.module_from_spec(spec)
        sys.modules["servo"] = self.servo
        spec.loader.exec_module(self.servo)
        self.servo.servo1 = types.SimpleNamespace(
            set_angle=lambda angle: self.record("gripper", angle)
        )
        self.servo.servo2 = types.SimpleNamespace(
            set_angle=lambda angle: self.record("lift", angle)
        )

    def record(self, *event):
        self.events.append(event)
        if self.fail_at_call == len(self.events):
            raise self.injected_error

    def assert_no_actuation(self):
        self.assertTrue(all(event == ("stop",) for event in self.events),
                        "Validation must precede servo or wheel movement")
        self.assertEqual(self.pwm_writes, [])

    def test_import_does_not_write_servo_positions(self):
        self.assert_no_actuation()

    def test_north_uses_upper_profile_and_reports_sequence_only(self):
        result = self.servo.northpole_dropoff("A3U", at_rack=True)
        self.assertEqual(self.events, expected_events(NORTH_TEST_PROFILE))
        self.assertEqual(result, {
            "target_node": "a3u",
            "pole": "north",
            "sequence_complete": True,
            "placement_confirmed": False,
        })

    def test_south_uses_distinct_lower_profile(self):
        result = self.servo.southpole_dropoff("B2L", at_rack=True)
        self.assertEqual(self.events, expected_events(SOUTH_TEST_PROFILE))
        self.assertEqual(result, {
            "target_node": "b2l",
            "pole": "south",
            "sequence_complete": True,
            "placement_confirmed": False,
        })

    def test_compatibility_aliases_forward_confirmation_and_result(self):
        for name, node, profile, pole in (
            ("north_pole_dropoff", "a1u", NORTH_TEST_PROFILE, "north"),
            ("south_pole_dropoff", "b6l", SOUTH_TEST_PROFILE, "south"),
            ("southpole", "a4l", SOUTH_TEST_PROFILE, "south"),
        ):
            with self.subTest(alias=name):
                self.events.clear()
                result = getattr(self.servo, name)(node, at_rack=True)
                self.assertEqual(self.events, expected_events(profile))
                self.assertEqual(result["pole"], pole)
                self.assertEqual(result["target_node"], node)

    def test_explicit_at_rack_confirmation_is_required(self):
        for name, node in (
            ("northpole_dropoff", "a1u"),
            ("southpole_dropoff", "b1l"),
            ("north_pole_dropoff", "a1u"),
            ("south_pole_dropoff", "b1l"),
            ("southpole", "a1l"),
        ):
            for confirmation in (False, None, "yes"):
                with self.subTest(function=name, at_rack=confirmation):
                    self.events.clear()
                    with self.assertRaises((TypeError, ValueError)):
                        getattr(self.servo, name)(node, at_rack=confirmation)
                    self.assert_no_actuation()
            with self.subTest(function=name, at_rack="omitted"):
                self.events.clear()
                with self.assertRaises((TypeError, ValueError)):
                    getattr(self.servo, name)(node)
                self.assert_no_actuation()

    def test_invalid_targets_cannot_move_robot(self):
        for name, targets in (
            ("northpole_dropoff", [None, 3, "", "c0", "a0u", "b7u", "c3u", "a3l"]),
            ("southpole_dropoff", [None, 3, "", "c0", "a0l", "b7l", "c3l", "a3u"]),
        ):
            for target in targets:
                with self.subTest(function=name, target=target):
                    self.events.clear()
                    with self.assertRaises((TypeError, ValueError)):
                        getattr(self.servo, name)(target, at_rack=True)
                    self.assert_no_actuation()

    def test_every_unknown_calibration_is_rejected_before_actuation(self):
        for name, node, profile in (
            ("northpole_dropoff", "a1u", self.calibration.NORTHPOLE_DROPOFF),
            ("southpole_dropoff", "b6l", self.calibration.SOUTHPOLE_DROPOFF),
        ):
            for key in tuple(profile):
                with self.subTest(function=name, parameter=key):
                    self.events.clear()
                    original = profile[key]
                    profile[key] = None
                    try:
                        with self.assertRaises((TypeError, ValueError)):
                            getattr(self.servo, name)(node, at_rack=True)
                        self.assert_no_actuation()
                    finally:
                        profile[key] = original

    def test_invalid_numbers_are_rejected_in_every_parameter(self):
        profile = self.calibration.NORTHPOLE_DROPOFF
        for key in tuple(profile):
            invalid_values = [True, False, float("nan"), float("inf"),
                              float("-inf"), "10", -1]
            if "angle" in key:
                invalid_values.append(self.servo.Servo.MAX_ANGLE + 1)
            else:
                invalid_values.append(0)
            if "speed" in key:
                invalid_values.append(101)
            for value in invalid_values:
                with self.subTest(parameter=key, value=value):
                    self.events.clear()
                    original = profile[key]
                    profile[key] = value
                    try:
                        with self.assertRaises((TypeError, ValueError)):
                            self.servo.northpole_dropoff("a1u", at_rack=True)
                        self.assert_no_actuation()
                    finally:
                        profile[key] = original

    def test_missing_calibration_key_cannot_move_robot(self):
        profile = self.calibration.NORTHPOLE_DROPOFF
        for key in tuple(profile):
            with self.subTest(parameter=key):
                self.events.clear()
                original = profile.pop(key)
                try:
                    with self.assertRaises((KeyError, TypeError, ValueError)):
                        self.servo.northpole_dropoff("a1u", at_rack=True)
                    self.assert_no_actuation()
                finally:
                    profile[key] = original

    def test_all_stage_failures_stop_without_running_later_stages(self):
        expected = expected_events(NORTH_TEST_PROFILE)
        for error_type in (RuntimeError, KeyboardInterrupt):
            for event_index, event in enumerate(expected[:-1]):
                if event == ("stop",):
                    continue
                with self.subTest(error=error_type.__name__, event=event,
                                  event_index=event_index):
                    self.events.clear()
                    self.fail_at_call = event_index + 1
                    self.injected_error = error_type("Injected stage failure")
                    with self.assertRaises(error_type):
                        self.servo.northpole_dropoff("a1u", at_rack=True)
                    self.assertEqual(self.events, expected[:event_index + 1] + [("stop",)])
        self.fail_at_call = None

    def test_servo_then_real_motion_can_be_imported_without_a_cycle(self):
        # Import real definitions only; config/utime/machine remain fakes.
        fake_config = types.ModuleType("config")
        fake_utime = types.ModuleType("utime")
        fake_utime.sleep = lambda seconds: self.record("sleep", seconds)
        fake_utime.ticks_ms = lambda: 0
        fake_utime.ticks_diff = lambda end, start: end - start
        with mock.patch.dict(sys.modules, {"config": fake_config, "utime": fake_utime}):
            with mock.patch.object(sys, "path", [str(ROOT)] + sys.path):
                sys.modules.pop("servo", None)
                sys.modules.pop("motion", None)
                servo = importlib.import_module("servo")
                motion = importlib.import_module("motion")
                self.assertTrue(callable(servo.northpole_dropoff))
                self.assertTrue(callable(motion.stop))
                self.assert_no_actuation()


if __name__ == "__main__":
    unittest.main()
