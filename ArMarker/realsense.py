import pyrealsense2 as rs

ctx = rs.context()
devices = ctx.query_devices()

if len(devices) == 0:
    print("RealSenseが見つかりません")
else:
    print(f"{len(devices)} 台見つかりました")

    for dev in devices:
        print("名前 :", dev.get_info(rs.camera_info.name))
        print("シリアル :", dev.get_info(rs.camera_info.serial_number))