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

    return path

print(breadth_first_search_algo("c0","r5"))