from config import vl53l0
from utime import sleep

print("Starting vl53l0...")

# Start device
vl53l0.start()

# Read ten samples
for _ in range(10):
    distance = vl53l0.read()
    print(f"Distance = {distance}mm")  # Check calibration!
    sleep(0.5)

# Stop device
vl53l0.stop()
