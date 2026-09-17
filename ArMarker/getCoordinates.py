#カラー画像と深度カメラの対応コード
#Arucoマーカーの中心座標を取得するコード
#カラー画像の中心座標は深度カメラに対応していないので注意

import cv2
import pyrealsense2 as rs
import numpy as np

# ============================================================
# 1. OpenCV：D435のColorカメラを起動
# ============================================================

cap = cv2.VideoCapture("/dev/video4", cv2.CAP_V4L2)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

if not cap.isOpened():
    print("Colorカメラを開けませんでした")
    exit()

# ============================================================
# 2. RealSense：Depthのみ起動
# ============================================================

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(
    rs.stream.depth,
    640,
    480,
    rs.format.z16,
    30
)

profile = pipeline.start(config)

# Depthセンサーのスケールを取得
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

print("Depth Scale:", depth_scale)

# ============================================================
# 3. ArUco設定
# ============================================================

dictionary = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_4X4_50
)

parameters = cv2.aruco.DetectorParameters()

detector = cv2.aruco.ArucoDetector(
    dictionary,
    parameters
)

# ============================================================
# 4. Depthカメラの内部パラメータ
# ============================================================

depth_profile = profile.get_stream(
    rs.stream.depth
)

depth_intrinsics = depth_profile.as_video_stream_profile().get_intrinsics()

print("--------------------------------")
print("Depth Camera Intrinsics")
print("fx =", depth_intrinsics.fx)
print("fy =", depth_intrinsics.fy)
print("cx =", depth_intrinsics.ppx)
print("cy =", depth_intrinsics.ppy)
print("--------------------------------")

print("ArUco + Depth detection start")
print("終了するには q を押してください")

# ============================================================
# 5. メインループ
# ============================================================

try:

    while True:

        # ----------------------------------------------------
        # Color画像を取得
        # ----------------------------------------------------

        ret, color_image = cap.read()

        if not ret:
            print("Color画像を取得できません")
            continue

        # ----------------------------------------------------
        # Depth画像を取得
        # ----------------------------------------------------

        frames = pipeline.wait_for_frames()

        depth_frame = frames.get_depth_frame()

        if not depth_frame:
            print("Depth画像を取得できません")
            continue

        # ----------------------------------------------------
        # ArUco検出
        # ----------------------------------------------------

        corners, ids, rejected = detector.detectMarkers(
            color_image
        )

        if ids is not None:

            # マーカーを描画
            cv2.aruco.drawDetectedMarkers(
                color_image,
                corners,
                ids
            )

            # 検出されたマーカーを処理
            for i, marker_id in enumerate(ids):

                # --------------------------------------------
                # ArUcoの4隅
                # --------------------------------------------

                points = corners[i][0]

                # --------------------------------------------
                # 中心座標
                # --------------------------------------------

                center_x = int(np.mean(points[:, 0]))
                center_y = int(np.mean(points[:, 1]))

                # --------------------------------------------
                # 中心位置を画像に描画
                # --------------------------------------------

                cv2.circle(
                    color_image,
                    (center_x, center_y),
                    5,
                    (0, 0, 255),
                    -1
                )

                # --------------------------------------------
                # Depthを取得
                # --------------------------------------------

                depth_value = depth_frame.get_distance(
                    center_x,
                    center_y
                )

                # --------------------------------------------
                # 3次元座標を計算
                # --------------------------------------------

                if depth_value > 0:

                    point_3d = rs.rs2_deproject_pixel_to_point(
                        depth_intrinsics,
                        [center_x, center_y],
                        depth_value
                    )

                    X = point_3d[0]
                    Y = point_3d[1]
                    Z = point_3d[2]

                    # ----------------------------------------
                    # ターミナル表示
                    # ----------------------------------------

                    print(
                        f"ID={marker_id[0]} "
                        f"Pixel=({center_x}, {center_y}) "
                        f"Depth={depth_value:.3f} m "
                        f"XYZ=({X:.3f}, {Y:.3f}, {Z:.3f})"
                    )

                    # ----------------------------------------
                    # 画像に表示
                    # ----------------------------------------

                    cv2.putText(
                        color_image,
                        f"ID: {marker_id[0]}",
                        (center_x + 10, center_y - 35),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        color_image,
                        f"Depth: {depth_value:.3f} m",
                        (center_x + 10, center_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        color_image,
                        f"X: {X:.3f} Y: {Y:.3f} Z: {Z:.3f}",
                        (center_x + 10, center_y + 15),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.45,
                        (0, 255, 0),
                        2
                    )

                else:

                    cv2.putText(
                        color_image,
                        "Depth: invalid",
                        (center_x + 10, center_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 255),
                        2
                    )

        # ----------------------------------------------------
        # Color画像を表示
        # ----------------------------------------------------

        cv2.imshow(
            "D435 ArUco + Depth",
            color_image
        )

        # qで終了
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:

    cap.release()
    pipeline.stop()
    cv2.destroyAllWindows()