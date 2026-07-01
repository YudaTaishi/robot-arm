#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pyrealsense2 as rs

# ==========================
# ArUco設定
# ==========================
aruco = cv2.aruco

dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(dictionary, parameters)

# ==========================
# RealSense設定
# ==========================
pipeline = rs.pipeline()
config = rs.config()

# カラー画像（640×480, 30fps）
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

pipeline.start(config)

print("RealSenseを起動しました。")
print("qキーで終了します。")

try:
    while True:

        # フレーム取得
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        # OpenCV画像へ変換
        frame = np.asanyarray(color_frame.get_data())

        # ==========================
        # ArUco検出
        # ==========================
        corners, ids, rejected = detector.detectMarkers(frame)

        if ids is not None:

            # マーカー枠を描画
            aruco.drawDetectedMarkers(frame, corners, ids)

            # ID表示
            for i in range(len(ids)):

                marker_id = ids[i][0]

                # マーカー中心座標
                corner = corners[i][0]

                center_x = int(corner[:, 0].mean())
                center_y = int(corner[:, 1].mean())

                print(f"検出ID : {marker_id}")

                cv2.putText(
                    frame,
                    f"ID:{marker_id}",
                    (center_x, center_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                )

                cv2.circle(frame, (center_x, center_y), 4, (255, 0, 0), -1)

        # ==========================
        # 画面表示
        # ==========================
        cv2.imshow("RealSense ArUco Detection", frame)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break

finally:

    pipeline.stop()
    cv2.destroyAllWindows()