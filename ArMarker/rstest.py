import pyrealsense2 as rs


def print_camera_info(device):
    """
    接続されたRealSenseデバイスの情報を表示する関数

    Args:
        device: pyrealsense2.device オブジェクト
    """
    print("-" * 40)
    print("Device Information:")
    print(f"  Name: {device.get_info(rs.camera_info.name)}")
    print(f"  Serial Number: {device.get_info(rs.camera_info.serial_number)}")
    print(f"  Firmware Version: {device.get_info(rs.camera_info.firmware_version)}")
    print(f"  Product Line: {device.get_info(rs.camera_info.product_line)}")
    print(f"  USB Type: {device.get_info(rs.camera_info.usb_type_descriptor)}")


try:
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()

    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()

    # 接続されたデバイスの情報を表示
    print_camera_info(device)

    device_product_line = str(device.get_info(rs.camera_info.product_line))

    found_rgb = False
    for s in device.sensors:
        if s.get_info(rs.camera_info.name) == 'RGB Camera':
            found_rgb = True
            break

    if not found_rgb:
        print("The demo requires Depth camera with Color sensor")
        exit(0)

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    if device_product_line == 'L500':
        config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
    else:
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)
    
    profile = pipeline.get_active_profile()

    print("=== Active Streams ===")
    for stream in profile.get_streams():
        vsp = stream.as_video_stream_profile()
        print(
            stream.stream_name(),
            vsp.width(),
            "x",
            vsp.height(),
            "@",
            vsp.fps()
        )
        print("RealSense camera connected and streaming.")

    try:
        # Allow the camera to warm up
        for _ in range(30):  # Get about 30 frames
            #pipeline.wait_for_frames()
            #タイムアウトエラー解消のためだったがあまり意味はない
            while True:
                flag,frames = pipeline.try_wait_for_frames()
                if flag == False: break


        print("Capturing a frame...")
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            print("Failed to capture frames.")
            exit(1)

        print("Frames captured successfully!")

    finally:
        # Stop streaming
        pipeline.stop()
        print("RealSense camera disconnected.")

except Exception as e:
    # Handle other potential errors
    print(f"An error occurred: {e}")
    exit(1)