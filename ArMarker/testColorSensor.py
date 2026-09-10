import pyrealsense2 as rs
import numpy as np
import cv2

# ==========================================
# RealSense 初期化
# ==========================================
pipeline = rs.pipeline()
config = rs.config()

# カラーセンサのみ
config.enable_stream(
    rs.stream.color,
    640,
    480,
    rs.format.bgr8,
    30
)

try:
    print("カラーセンサを起動しています...")

    pipeline.start(config)

    print("カラーセンサの起動に成功しました")
    print("映像を表示します")
    print("終了するには q を押してください")

    while True:

        # フレーム取得
        frames = pipeline.wait_for_frames()

        # カラーフレーム
        color_frame = frames.get_color_frame()

        if not color_frame:
            print("カラー画像を取得できません")
            continue

        # numpy配列に変換
        color_image = np.asanyarray(
            color_frame.get_data()
        )

        # 表示
        cv2.imshow(
            "RealSense Color",
            color_image
        )

        # qで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
    print("終了しました")