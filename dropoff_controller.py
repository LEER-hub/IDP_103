"""Sensor-driven delivery workflow with injected hardware/navigation functions."""


class DropoffController:
    """Deliver one item per run_once() call.

    navigate(start, end) must drive between mapped nodes, stop at end, and
    return only when travel completes. It must not pick up or release cargo.
    is_occupied(bay) must aim/read the distance sensor from the adjacent
    junction without entering the bay; return 1 (occupied) or 0 (empty).
    read_pole() returns 'north' or 'south' while stopped at the pickup node.
    Hardware callbacks must raise on failures rather than report success.
    """

    def __init__(self, navigate, read_pole, is_occupied, pickup, dropoff,
                 stop, side="right", start_node="c0"):
        if side not in ("right", "left"):
            raise ValueError("side must be 'right' or 'left'")
        self.navigate = navigate
        self.read_pole = read_pole
        self.is_occupied = is_occupied
        self.pickup = pickup
        self.dropoff = dropoff
        self.stop = stop
        self.side = side
        self.current_node = start_node
        self.pickup_node = "la3" if side == "right" else "la2"
        self.return_node = "la4" if side == "right" else "la1"
        self.filled_bays = set()
        self.carrying = False
        self.pole = None

    def _move_to(self, destination):
        if self.current_node != destination:
            self.navigate(self.current_node, destination)
            self.current_node = destination
        self.stop()

    def _rows(self):
        rack = "b" if self.side == "right" else "a"
        if self.pole == "south":
            return [("r" if self.side == "right" else "l", rack, "l")]
        other_rack = "a" if rack == "b" else "b"
        return [("c", rack, "u"), ("c", other_rack, "u")]

    def run_once(self):
        """Pick, scan, release, and return; return the bay or None if full.

        When full, return to the pickup node with cargo still held. A later
        call retries scanning without picking up another item. Locally filled
        bays persist for this controller's lifetime; map nodes are not deleted.
        """
        try:
            if not self.carrying:
                self._move_to(self.pickup_node)
                pole = self.read_pole()
                if pole not in ("north", "south"):
                    raise ValueError("No valid magnetic pole detected")
                self.pole = pole
                self.pickup()
                self.carrying = True

            for junction_prefix, rack, level in self._rows():
                for current_number in range(1, 7):
                    number = str(current_number)
                    junction = junction_prefix + number
                    bay = rack + number + level
                    if bay in self.filled_bays:
                        continue
                    self._move_to(junction)
                    occupied = self.is_occupied(bay)
                    if occupied is None or occupied not in (0, 1):
                        raise ValueError("Distance callback must return 0 or 1")
                    if occupied == 1:
                        continue
                    self._move_to(bay)
                    self.dropoff()
                    self.filled_bays.add(bay)
                    self.carrying = False
                    self.pickup_node = self.return_node
                    self._move_to(self.return_node)
                    return bay

            self._move_to(self.pickup_node)
            return None
        finally:
            self.stop()
