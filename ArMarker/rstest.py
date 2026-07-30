import pyrealsense2 as rs


pipeline = rs.pipeline()
config = rs.config()


config.enable_stream(
    rs.stream.depth,
    640,
    480,
    rs.format.z16,
    30
)


pipeline.start(config)


try:
    while True:

        frames = pipeline.wait_for_frames(
            timeout_ms=10000
        )

        depth_frame = frames.get_depth_frame()

        if not depth_frame:
            continue


        width = depth_frame.get_width()
        height = depth_frame.get_height()


        dist = depth_frame.get_distance(
            width // 2,
            height // 2
        )


        print(
            f"Distance: {dist:.3f} m",
            end="\r"
        )


finally:
    pipeline.stop()