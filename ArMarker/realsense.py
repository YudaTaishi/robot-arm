import pyrealsense2 as rs

ctx = rs.context()
print(ctx.devices.size())

for dev in ctx.devices:
    print(dev.get_info(rs.camera_info.name))