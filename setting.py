from pymycobot.mycobot import MyCobot
import time

mc = MyCobot("/dev/ttyAMA0", 115200)

time.sleep(2)

print("Version:", mc.get_system_version())
print("Angles :", mc.get_angles())
print("Coords :", mc.get_coords())
print("Power  :", mc.is_power_on())