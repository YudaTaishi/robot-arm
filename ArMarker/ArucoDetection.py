import pyrealsense2 as rs
import numpy as np
import cv2


# ==============================
# RealSense 初期化
# ==============================
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


try:

    while True:

        frames = pipeline.wait_for_frames()

        color_frame = frames.get_color_frame()

        if not color_frame:
            continue


        # ==============================
        # YUYVデータ取得
        # ==============================
        yuyv = np.asanyarray(color_frame.get_data())


        # 確認用
        # print(yuyv.shape)


        # ==============================
        # YUYV形式をOpenCV用に変換
        # ==============================
        if len(yuyv.shape) == 2:

            # (480,640) → (480,640,2)
            yuyv = yuyv.reshape(
                (480, 640, 2)
            )


        color_image = cv2.cvtColor(
            yuyv,
            cv2.COLOR_YUV2BGR_YUYV
        )


        # ==============================
        # 表示
        # ==============================
        cv2.imshow(
            "RealSense Color",
            color_image
        )


        if cv2.waitKey(1) & 0xFF == 27:
            break


finally:

    pipeline.stop()
    cv2.destroyAllWindows()