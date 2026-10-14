import pyrealsense2 as rs
import time

tests = [
    ("depth_only", True, False, 640, 480, 30),
    ("color_only", False, True, 640, 480, 30),
    ("depth_color", True, True, 640, 480, 30),
]

ctx = rs.context()
devices = ctx.query_devices()

for device in devices:
    print("Device:", device.get_info(rs.camera_info.name))
    print("Firmware:", device.get_info(rs.camera_info.firmware_version))
    print("USB:", device.get_info(rs.camera_info.usb_type_descriptor))

for name, depth, color, width, height, fps in tests:
    print(f"\n===== {name} =====")

    pipeline = rs.pipeline()
    config = rs.config()

    if depth:
        config.enable_stream(
            rs.stream.depth, width, height, rs.format.z16, fps
        )

    if color:
        config.enable_stream(
            rs.stream.color, width, height, rs.format.bgr8, fps
        )

    started = False

    try:
        pipeline.start(config)
        started = True
        print("Pipeline started")

        for i in range(10):
            frames = pipeline.wait_for_frames(10000)
            print(
                f"{i}: depth={bool(frames.get_depth_frame())}, "
                f"color={bool(frames.get_color_frame())}"
            )

        print("RESULT: SUCCESS")

    except Exception as e:
        print("RESULT: FAILED")
        print(type(e).__name__, str(e))

    finally:
        if started:
            pipeline.stop()

    time.sleep(2)