import pyrealsense2 as rs
import numpy as np
import cv2


pipeline = rs.pipeline()
config = rs.config()


config.enable_stream(
    rs.stream.color,
    848,
    480,
    rs.format.bgr8,
    30
)


pipeline.start(config)


while True:

    frames = pipeline.wait_for_frames()

    color_frame = frames.get_color_frame()

    if not color_frame:
        continue


    color_image = np.asanyarray(
        color_frame.get_data()
    )


    print(color_image.shape)


    cv2.imshow(
        "RealSense Color",
        color_image
    )


    if cv2.waitKey(1) == 27:
        break


pipeline.stop()
cv2.destroyAllWindows()