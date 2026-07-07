import cv2
import numpy as np
import pyrealsense2 as rs

# ==============================
# RealSense 初期化
# ==============================
pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

pipeline.start(config)

# ==============================
# ArUco辞書設定
# ==============================
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

print("ESCキーで終了")

try:
    while True:

        # ==============================
        # カメラ画像取得
        # ==============================
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        image = np.asanyarray(color_frame.get_data())

        # ==============================
        # ArUco検出
        # ==============================
        corners, ids, rejected = detector.detectMarkers(image)

        if ids is not None:

            cv2.aruco.drawDetectedMarkers(image, corners, ids)

            for i in range(len(ids)):
                marker_id = int(ids[i][0])

                print(f"検出したマーカーID : {marker_id}")

                corner = corners[i][0]

                center_x = int(np.mean(corner[:, 0]))
                center_y = int(np.mean(corner[:, 1]))

                cv2.putText(
                    image,
                    f"ID:{marker_id}",
                    (center_x, center_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2,
                )

        # ==============================
        # 表示
        # ==============================
        cv2.imshow("RealSense ArUco Detection", image)

        key = cv2.waitKey(1)
        if key == 27:   # ESC
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()