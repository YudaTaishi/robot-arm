import numpy as np
import cv2


# ==============================
# RealSense 初期化
# ==============================
pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)

config.enable_stream(
    rs.stream.color,
    848,
    480,
    rs.format.bgr8,
    30
)
profile = pipeline.start(config)

# 深度画像をカラー画像の座標系に合わせる
align = rs.align(rs.stream.color)

pipeline.start(config)
# カラーカメラの内部パラメータ（3D復元に使用）
intrinsics = profile.get_stream(
    rs.stream.color
).as_video_stream_profile().get_intrinsics()

# ==============================
# ArUco 辞書設定
# ==============================
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

while True:

    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

    frames = pipeline.wait_for_frames()
    print("ESCキーで終了")

    color_frame = frames.get_color_frame()
    try:
        while True:

    if not color_frame:
         continue
        # ==============================
        # フレーム取得（深度をカラーに整列）
        # ==============================
        frames = pipeline.wait_for_frames()
        frames = align.process(frames)

        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        color_image = np.asanyarray(
          color_frame.get_data()
        )
        if not color_frame or not depth_frame:
            continue

        image = np.asanyarray(color_frame.get_data())

    print(color_image.shape)
        # ==============================
        # ArUco 検出
        # ==============================
        corners, ids, rejected = detector.detectMarkers(image)

        if ids is not None:

    cv2.imshow(
        "RealSense Color",
        color_image
    )
            cv2.aruco.drawDetectedMarkers(image, corners, ids)

            for i in range(len(ids)):
                marker_id = int(ids[i][0])

    if cv2.waitKey(1) == 27:
        break
                corner = corners[i][0]

                center_x = int(np.mean(corner[:, 0]))
                center_y = int(np.mean(corner[:, 1]))

pipeline.stop()
cv2.destroyAllWindows()
 No newline at end of file
                # マーカ中心までの距離[m]
                depth = depth_frame.get_distance(center_x, center_y)

                # ピクセル座標 + 深度 → カメラ座標系の3D点[m]
                point = rs.rs2_deproject_pixel_to_point(
                    intrinsics,
                    [center_x, center_y],
                    depth,
                )

                x, y, z = point

                print(
                    f"ID:{marker_id}  "
                    f"距離={depth:.3f}m  "
                    f"XYZ=({x:.3f}, {y:.3f}, {z:.3f})"
                )

                cv2.circle(image, (center_x, center_y), 5, (0, 0, 255)
, -1)

                cv2.putText(
                    image,
                    f"ID:{marker_id} {depth:.2f}m",
                    (center_x + 10, center_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
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