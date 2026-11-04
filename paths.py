from line_follower import nodes
import motion
tight_nodes = tuple(prefix + str(number) for prefix in ("c", "r", "l") for number in range(1, 7))
drop_nodes = tuple(node for node in nodes if node.endswith(("u", "l")))
short_nodes = ("la1", "la2", "la3", "la4")

right_nodes = [
    "s_e", "r0", "j_la3", "la3", "j_la4", "la4",
    "r1", "r2", "r3", "r4", "r5", "r6", "end_r",
    "b1u", "b2u", "b3u", "b4u", "b5u", "b6u",
    "b1l", "b2l", "b3l", "b4l", "b5l", "b6l",
]

COMPASS = ("north", "east", "south", "west")


def get_turn(current_node, next_node, heading):
    target_direction = nodes[current_node][next_node]
    target_heading = COMPASS.index(target_direction)
    return (target_heading - heading) % 4

def nodeskip(previous_node,current_node, next_node):
    if (previous_node in drop_nodes) and (current_node in tight_nodes) and not (next_node in ("j_la4","s_n","j_la1"))                                                                                                                                                                                               :
        return True
    else:
        return False

right_close_pickup = ["c0","s_e","r0","j_la3","la3","j_la3","r0"]
right_far_pickup = ["c0","s_e","r0","j_la3","j_la4","la4","j_la4","j_la3","r0"]
#detect magnet

right_south = ["j_la3","j_la4","r1"]
right_north = ["s_e","c0","s_n","c1"]

lower_right_dropoff_path = [] #start at r1
upper_right_dropoff_path = [] #start at C1
upper_left_dropoff_path = [] #start at c1
lower_left_dropoff_path = [] # start at l1
# 1 if b1l has been delivered to, then we skip on to r2
#loop through all Rs
#if not full, then deliver
#return to R1.
#go to j_la4, la4, j_la4
#if south pole then run #1 

left_pickup = ["c0","s_w","l0","j_la2","la2","j_la2"]
right_dropoff = []

hardcode_path = ["c0","s_e","r0","j_la3","la3","j_la3","j_la4","r1","r2","b2l","r2","r1","j_la4","j_la3","r0","s_e","c0",
        "s_w","l0","j_la2","la2", "j_la2","j_la1","l1","l2","a2l","l2","l1","j_la1","j_la2","l0","s_w","c0",
        "s_e","r0","j_la3","j_la4","la4","j_la4","r1","r2","r3","b3l","r3","r2","r1","j_la4","j_la3","r0","s_e","c0",
        "s_w","l0","j_la2","j_la1","la1","j_la1","l1","a1l","l1","j_la1","j_la2","l0","s_w","c0"]

def get_right_dropoff(polarity):
    if polarity == "north":
        return upper_right_dropoff_path
    elif polarity == "south":
        return lower_right_dropoff_path
    return None

def get_left_dropoff(polarity):
    if polarity == "north":
        return upper_left_dropoff_path
    elif polarity == "south":
        return lower_left_dropoff_path
    return None

def breadth_first_search_algo (start_node, target_node):
    queue = [start_node]
    visited = {start_node}
    previous = {start_node: None}
    
    while len(queue) > 0:
        node = queue.pop(0)
        if node == target_node:
                    path = []
                    while node is not None:
                        path.append(node)
                        node = previous[node]
                    path.reverse()
                    return path
        
        for neighbour in nodes[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
                previous[neighbour] = node

    return None

boxheld_previous = 0
boxheld_current = 0
path = []
path.extend(breadth_first_search_algo("c0","la3"))
available_dropoff_nodes_right_lower = ["b2l","b4l","b6l","b3l","b5l"]
available_dropoff_nodes_right_upper = ["b2u","b4u","b6u","b3u","b5u"]
available_dropoff_nodes_left_lower = ["a2l","a4l","a6l","a1l","a3l","a5l"]
available_dropoff_nodes_left_upper = ["a2u","a4u","a6u","a1u","a3u","a5u"]
right_pickup_nodes = ["la4","la3","j_la4","j_la3"]
left_pickup_nodes = ["la1","la2","j_la1","j_la2"]
upper_nodes = ["b1u","b2u","b3u","b4u","b5u","b6u","a1u","a2u","a3u","a4u","a5u","a6u","c1","c2","c3","c4","c5","c6"]


def plan_available_dropoff(current_node, polarity, side):
    if side == "right":
        if polarity == "north":
            available_nodes = available_dropoff_nodes_right_upper
        elif polarity == "south":
            available_nodes = available_dropoff_nodes_right_lower
        else:
            raise ValueError("Invalid polarity")

    elif side == "left":
        if polarity == "north":
            available_nodes = available_dropoff_nodes_left_upper
        elif polarity == "south":
            available_nodes = available_dropoff_nodes_left_lower
        else:
            raise ValueError("Invalid polarity")

    else:
        raise ValueError("Invalid side")

    if not available_nodes:
        return None, None

    target_bay = available_nodes[0]
    route = breadth_first_search_algo(current_node, target_bay)
    return route, target_bay

def bay_unavailable(bay):
    if bay in available_dropoff_nodes_right_lower:
        available_dropoff_nodes_right_lower.remove(bay)
    elif bay in available_dropoff_nodes_right_upper:
        available_dropoff_nodes_right_upper.remove(bay)
    elif bay in available_dropoff_nodes_left_lower:
        available_dropoff_nodes_left_lower.remove(bay)
    elif bay in available_dropoff_nodes_left_upper:
        available_dropoff_nodes_left_upper.remove(bay)
    return
    
#robot path appender pseudocode
'''
The challenge: we now want to integrate magent sensor and distance sensor to see where we need to 
deliver to and where the boxes are full

1. create a list of all possible dropoff nodes.
2. append in a path to pickup a box
3. execute pickup of the box
4. read polarity using magnet sensor
5. if magnet sensor is south head to node r1
    if magnet sensor reading is north head to c1
 execute the available node finder algorithm


Available node finder algorithm:
1. robot goes to the first branch
2. robot heads towards the dropoff node while reading box distance
3. if box distance reaches within a certain threshold assum we detect a box and then strike it off
the list of available dropoff nodes
4. make the target node equal the next available node
5. head to that next available node and keep repeating the process until we find a truly free node
and drop off the parcel.
'''
