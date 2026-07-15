import pyrealsense2 as rs

ctx = rs.context()
devices = ctx.query_devices()

print("接続台数:", len(devices))

for dev in devices:
    print(dev.get_info(rs.camera_info.name))
    print(dev.get_info(rs.camera_info.serial_number))