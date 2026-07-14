import pyrealsense2 as rs

ctx = rs.context()
dev = ctx.devices[0]

for sensor in dev.query_sensors():
    print(sensor.get_info(rs.camera_info.name))