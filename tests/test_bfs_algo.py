nodes = {
    # Start box
    "c0": {"s_n": "north", "s_e": "east", "s_w": "west"},
    "s_n": {"c1": "north", "s_ne": "east", "c0": "south", "s_nw": "west"},
    "s_ne": {"s_e": "south", "s_n": "west"},
    "s_e": {"s_ne": "north", "r0": "east", "s_se": "south", "c0": "west"},
    "s_se": {"s_e": "north", "s_sw": "west"},
    "s_sw": {"s_w": "north", "s_se": "east"},
    "s_w": {"s_nw": "north", "c0": "east", "s_sw": "south", "l0": "west"},
    "s_nw": {"s_n": "east", "s_w": "south"},

    # Left track: bottom to top
    "l0": {"j_la2": "north", "s_w": "east"},
    "j_la2": {"j_la1": "north", "la2": "east", "l0": "south"},
    "j_la1": {"l1": "north", "la1": "east", "j_la2": "south"},
    "l1": {"l2": "north", "a1l": "east", "j_la1": "south"},
    "l2": {"l3": "north", "a2l": "east", "l1": "south"},
    "l3": {"l4": "north", "a3l": "east", "l2": "south"},
    "l4": {"l5": "north", "a4l": "east", "l3": "south"},
    "l5": {"l6": "north", "a5l": "east", "l4": "south"},
    "l6": {"end_l": "north", "a6l": "east", "l5": "south"},
    "end_l": {"l6": "south"},

    # Centre track: bottom to top
    "c1": {"c2": "north", "b1u": "east", "s_n": "south", "a1u": "west"},
    "c2": {"c3": "north", "b2u": "east", "c1": "south", "a2u": "west"},
    "c3": {"c4": "north", "b3u": "east", "c2": "south", "a3u": "west"},
    "c4": {"c5": "north", "b4u": "east", "c3": "south", "a4u": "west"},
    "c5": {"c6": "north", "b5u": "east", "c4": "south", "a5u": "west"},
    "c6": {"end_c": "north", "b6u": "east", "c5": "south", "a6u": "west"},
    "end_c": {"c6": "south"},

    # Right track: bottom to top
    "r0": {"j_la3": "north", "s_e": "west"},
    "j_la3": {"j_la4": "north", "r0": "south", "la3": "west"},
    "j_la4": {"r1": "north", "j_la3": "south", "la4": "west"},
    "r1": {"r2": "north", "j_la4": "south", "b1l": "west"},
    "r2": {"r3": "north", "r1": "south", "b2l": "west"},
    "r3": {"r4": "north", "r2": "south", "b3l": "west"},
    "r4": {"r5": "north", "r3": "south", "b4l": "west"},
    "r5": {"r6": "north", "r4": "south", "b5l": "west"},
    "r6": {"end_r": "north", "r5": "south", "b6l": "west"},
    "end_r": {"r6": "south"},

    # Loading-area destinations
    "la1": {"j_la1": "west"},
    "la2": {"j_la2": "west"},
    "la3": {"j_la3": "east"},
    "la4": {"j_la4": "east"},

    # Rack A: outer side, accessed from the left track
    "a1l": {"l1": "west"},
    "a2l": {"l2": "west"},
    "a3l": {"l3": "west"},
    "a4l": {"l4": "west"},
    "a5l": {"l5": "west"},
    "a6l": {"l6": "west"},

    # Rack A: centre side, accessed from the centre track
    "a1u": {"c1": "east"},
    "a2u": {"c2": "east"},
    "a3u": {"c3": "east"},
    "a4u": {"c4": "east"},
    "a5u": {"c5": "east"},
    "a6u": {"c6": "east"},

    # Rack B: centre side, accessed from the centre track
    "b1u": {"c1": "west"},
    "b2u": {"c2": "west"},
    "b3u": {"c3": "west"},
    "b4u": {"c4": "west"},
    "b5u": {"c5": "west"},
    "b6u": {"c6": "west"},

    # Rack B: outer side, accessed from the right track
    "b1l": {"r1": "east"},
    "b2l": {"r2": "east"},
    "b3l": {"r3": "east"},
    "b4l": {"r4": "east"},
    "b5l": {"r5": "east"},
    "b6l": {"r6": "east"},
}




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