import pyrealsense2 as rs
import time

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(
    rs.stream.color,
    848,
    480,
    rs.format.yuyv,
    30
)

print("start")

pipeline.start(config)

print("started")

time.sleep(2)

for i in range(20):

    frames = pipeline.wait_for_frames(
        timeout_ms=5000
    )

    color = frames.get_color_frame()

    if color:
        print(
            i,
            "color OK",
            color.get_width(),
            color.get_height(),
            color.get_profile().format()
        )
    else:
        print(i,"no color")

pipeline.stop()