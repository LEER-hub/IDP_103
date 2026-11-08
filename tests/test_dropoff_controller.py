"""Desktop-only workflow tests; no machine/config imports required."""
import unittest

from dropoff_controller import DropoffController


class DropoffControllerTests(unittest.TestCase):
    def make_controller(self, pole="south", occupied=None, side="right"):
        # Record actions through callbacks so the workflow can be checked without hardware.
        events = []
        occupied = occupied or (lambda bay: 0)
        controller = DropoffController(
            lambda start, end: events.append(("move", start, end)),
            lambda: pole,
            occupied,
            lambda: events.append("pickup"),
            lambda: events.append("dropoff"),
            lambda: events.append("stop"),
            side=side,
        )
        return controller, events

    def test_skip_occupied_and_repeat_from_la4(self):
        controller, events = self.make_controller(
            occupied=lambda bay: int(bay == "b1l"))
        self.assertEqual(controller.run_once(), "b2l")
        self.assertEqual(controller.current_node, "la4")
        self.assertEqual(controller.run_once(), "b3l")
        self.assertEqual(events.count("pickup"), 2)
        self.assertEqual(events.count("dropoff"), 2)
        self.assertIn(("move", "c0", "la3"), events)
        self.assertNotIn(("move", "r1", "b1l"), events)

    def test_north_falls_back_to_other_rack(self):
        for side, full_rack, expected in (("right", "b", "a1u"),
                                          ("left", "a", "b1u")):
            checked = []

            def occupied(bay):
                checked.append(bay)
                return int(bay.startswith(full_rack))

            controller, _ = self.make_controller("north", occupied, side)
            self.assertEqual(controller.run_once(), expected)
            self.assertEqual(len(checked), 7)
            self.assertEqual(controller.current_node,
                             "la4" if side == "right" else "la1")

    def test_left_south(self):
        controller, events = self.make_controller(side="left")
        self.assertEqual(controller.run_once(), "a1l")
        self.assertIn(("move", "c0", "la2"), events)
        self.assertEqual(controller.current_node, "la1")

    def test_full_retains_cargo_and_retry_does_not_pick_again(self):
        controller, events = self.make_controller("north", lambda bay: 1)
        self.assertIsNone(controller.run_once())
        self.assertTrue(controller.carrying)
        self.assertEqual(controller.current_node, "la3")
        self.assertNotIn("dropoff", events)
        controller.is_occupied = lambda bay: 0
        self.assertEqual(controller.run_once(), "b1u")
        self.assertEqual(events.count("pickup"), 1)

    def test_invalid_pole_stops_before_pickup(self):
        controller, events = self.make_controller(None)
        with self.assertRaises(ValueError):
            controller.run_once()
        self.assertNotIn("pickup", events)
        self.assertEqual(events[-1], "stop")

    def test_invalid_distance_keeps_cargo_without_release(self):
        controller, events = self.make_controller(occupied=lambda bay: None)
        with self.assertRaises(ValueError):
            controller.run_once()
        self.assertTrue(controller.carrying)
        self.assertNotIn("dropoff", events)
        self.assertEqual(events[-1], "stop")


if __name__ == "__main__":
    unittest.main()
