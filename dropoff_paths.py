"""Drop-off targets and routes, without hardware dependencies."""

lower_right_dropoff = ["r1", "b1l", "r1"]
upper_right_dropoff = ["c1", "b1u", "c1"]
upper_left_dropoff = ["c1", "a1u", "c1"]
lower_left_dropoff = ["l1", "a1l", "l1"]


def _target(dropoff_path):
    if not dropoff_path:
        raise ValueError("All drop-off bays in this row are occupied")
    if len(dropoff_path) != 3:
        raise ValueError("Expected [junction, bay, junction]")
    junction, bay, return_junction = dropoff_path
    if not isinstance(junction, str) or not isinstance(bay, str):
        raise ValueError("Node names must be strings")
    if (junction != return_junction or len(junction) < 2 or
            not junction[1:].isdigit()):
        raise ValueError("Invalid drop-off junctions")
    number = int(junction[1:])
    prefix = junction[0]
    allowed_bays = {"r": ("b", "l"), "l": ("a", "l")}
    if prefix == "c":
        valid = bay in ("a" + str(number) + "u", "b" + str(number) + "u")
    elif prefix in allowed_bays:
        rack, level = allowed_bays[prefix]
        valid = bay == rack + str(number) + level
    else:
        valid = False
    if not valid or not 1 <= number <= 6:
        raise ValueError("Bay must match a mapped junction numbered 1 through 6")
    return prefix, number, bay[0], bay[-1]


def advance_dropoff(dropoff_path):
    """Call after a successful drop; mutate the same list to the next bay.

    An empty list means that all six bays in this row have been used.
    Traversal junctions stay in the map so later trips can pass through them.
    """
    prefix, number, rack, level = _target(dropoff_path)
    if number == 6:
        dropoff_path[:] = []
    else:
        next_number = str(number + 1)
        next_junction = prefix + next_number
        next_bay = rack + next_number + level
        dropoff_path[:] = [next_junction, next_bay, next_junction]
    return dropoff_path


def build_dropoff_route(dropoff_path):
    """Return a fresh route from the row entrance to the bay and back.

    For b2l: j_la4 -> r1 -> r2 -> b2l -> r2 -> r1 -> j_la4.
    Pickup at la4 is handled separately by the caller.
    """
    prefix, number, _, _ = _target(dropoff_path)
    entrance = {"r": "j_la4", "l": "j_la1", "c": "s_n"}[prefix]
    outward = [entrance] + [prefix + str(i) for i in range(1, number + 1)]
    return outward + [dropoff_path[1]] + outward[::-1]
