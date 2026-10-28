from line_follower import nodes
tight_nodes = tuple(prefix + str(number) for prefix in ("c", "r", "l") for number in range(1, 7))
drop_nodes = tuple(node for node in nodes if node.endswith(("u", "l")))
short_nodes = ("la1", "la2", "la3", "la4")

COMPASS = ("north", "east", "south", "west")


def get_turn(current_node, next_node, heading):
    target_direction = nodes[current_node][next_node]
    target_heading = COMPASS.index(target_direction)
    return (target_heading - heading) % 4

def nodeskip(previous_node,current_node, next_node):
    if (previous_node in drop_nodes) and (current_node in tight_nodes) and not (next_node in ("j_la4","s_n","j_la1")):
        return True
    else:
        return False