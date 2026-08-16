import cv2
import numpy as np
import pyrealsense2 as rs


# ==========================================
# RealSense 初期化
# ==========================================

pipeline = rs.pipeline()
config = rs.config()

# カラー画像
config.enable_stream(
    rs.stream.color,
    640, 480,
    rs.format.bgr8,
    30
)

# 深度画像
config.enable_stream(
    rs.stream.depth,
    640, 480,
    rs.format.z16,
    30
)

profile = pipeline.start(config)


# ==========================================
# Depth → Color の位置合わせ
# ==========================================

align = rs.align(rs.stream.color)


# ==========================================
# カメラ内部パラメータ
# ==========================================

color_profile = profile.get_stream(
    rs.stream.color
).as_video_stream_profile()

color_intrinsics = color_profile.get_intrinsics()


# ==========================================
# ArUco設定
# ==========================================

aruco_dict = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_4X4_50
)

parameters = cv2.aruco.DetectorParameters()

detector = cv2.aruco.ArucoDetector(
    aruco_dict,
    parameters
)


print("RealSense started.")
print("ArUco marker detection started.")
print("Press 'q' to quit.")


try:

    while True:

        # ==================================
        # フレーム取得
        # ==================================

        frames = pipeline.wait_for_frames()

        # DepthをColorに位置合わせ
        aligned_frames = align.process(frames)

        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue


        # ==================================
        # OpenCV画像へ変換
        # ==================================

        color_image = np.asanyarray(
            color_frame.get_data()
        )


        # ==================================
        # ArUco検出
        # ==================================

        corners, ids, rejected = detector.detectMarkers(
            color_image
        )


        # ==================================
        # マーカーが見つかった場合
        # ==================================

        if ids is not None:

            cv2.aruco.drawDetectedMarkers(
                color_image,
                corners,
                ids
            )


            for i, marker_id in enumerate(ids):

                # ------------------------------
                # マーカー4隅
                # ------------------------------

                corner = corners[i][0]

                # corner:
                # [0] 左上
                # [1] 右上
                # [2] 右下
                # [3] 左下

                # ------------------------------
                # マーカー中心座標
                # ------------------------------

                center_x = int(
                    np.mean(corner[:, 0])
                )

                center_y = int(
                    np.mean(corner[:, 1])
                )


                # ------------------------------
                # 中心画素の深度
                # ------------------------------

                depth = depth_frame.get_distance(
                    center_x,
                    center_y
                )


                # 深度が取得できなかった場合
                if depth <= 0:

                    print(
                        f"ID {marker_id[0]}: "
                        "Depth unavailable"
                    )

                    continue


                # ==================================
                # 画像座標 → 3次元座標
                # ==================================

                point_3d = rs.rs2_deproject_pixel_to_point(
                    color_intrinsics,
                    [center_x, center_y],
                    depth
                )


                X = point_3d[0]
                Y = point_3d[1]
                Z = point_3d[2]


                # ==================================
                # 座標表示
                # ==================================

                print(
                    f"ID {marker_id[0]} : "
                    f"X = {X:.3f} m, "
                    f"Y = {Y:.3f} m, "
                    f"Z = {Z:.3f} m"
                )


                # ==================================
                # 画像上に中心点を描画
                # ==================================

                cv2.circle(
                    color_image,
                    (center_x, center_y),
                    5,
                    (0, 0, 255),
                    -1
                )


                # ==================================
                # 画像上に座標表示
                # ==================================

                text = (
                    f"ID:{marker_id[0]} "
                    f"X:{X:.3f} "
                    f"Y:{Y:.3f} "
                    f"Z:{Z:.3f}"
                )

                cv2.putText(
                    color_image,
                    text,
                    (center_x - 100, center_y - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )


        # ==================================
        # 画像表示
        # ==================================

        cv2.imshow(
            "RealSense ArUco",
            color_image
        )


        # qキーで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


finally:

    pipeline.stop()
    cv2.destroyAllWindows()