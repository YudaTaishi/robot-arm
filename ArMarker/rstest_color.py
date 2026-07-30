import pyrealsense2 as rs

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(
    rs.stream.color,
    640,
    480,
    rs.format.yuyv,
    30
)

pipeline.start(config)

print("start OK")

for i in range(10):
    frames = pipeline.wait_for_frames()
    color = frames.get_color_frame()

    if color:
        print("color frame OK", i)
    else:
        print("no color")

pipeline.stop()