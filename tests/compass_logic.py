compass = ["north", "east", "south", "west"]

tracker = 0

for i in range(20):
    tracker += 1
    remainder = tracker%4
    heading = compass[remainder]
    print (heading)
