import pyrealsense2 as rs
import numpy as np
import cv2


pipeline = rs.pipeline()
config = rs.config()


config.enable_stream(
    rs.stream.color,
    848,
    480,
    rs.format.yuyv,
    30
)


pipeline.start(config)


while True:

    frames = pipeline.wait_for_frames()

    color_frame = frames.get_color_frame()

    if not color_frame:
        continue


    # 取得データ
    yuyv = np.asanyarray(
        color_frame.get_data()
    )


    print("shape:", yuyv.shape)


    # YUYV形式へ修正
    if len(yuyv.shape) == 2:

        yuyv = yuyv.reshape(
            480,
            848,
            2
        )


    # YUYV → BGR
    color_image = cv2.cvtColor(
        yuyv,
        cv2.COLOR_YUV2BGR_YUYV
    )


    cv2.imshow(
        "RealSense Color",
        color_image
    )


    if cv2.waitKey(1) == 27:
        break


pipeline.stop()
cv2.destroyAllWindows()