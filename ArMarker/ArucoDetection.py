#OpenCVで取得したカラー画像からAruco検出

import cv2

# ==========================================
# Camera settings
# ==========================================
cap = cv2.VideoCapture("/dev/video4", cv2.CAP_V4L2)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

if not cap.isOpened():
    print("カメラを開けませんでした")
    exit()

# ==========================================
# ArUco settings
# ==========================================
dictionary = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_4X4_50
)

parameters = cv2.aruco.DetectorParameters()

detector = cv2.aruco.ArucoDetector(
    dictionary,
    parameters
)

print("ArUco検出を開始します")
print("終了するには q を押してください")

# ==========================================
# Main loop
# ==========================================
while True:

    ret, frame = cap.read()

    if not ret:
        print("フレームを取得できません")
        continue

    # --------------------------------------
    # ArUco marker detection
    # --------------------------------------
    corners, ids, rejected = detector.detectMarkers(frame)

    # マーカーが検出された場合
    if ids is not None:

        # マーカーを画像に描画
        cv2.aruco.drawDetectedMarkers(
            frame,
            corners,
            ids
        )

        # 検出されたマーカーごとに処理
        for i, marker_id in enumerate(ids):

            # 4隅の座標
            points = corners[i][0]

            # 中心座標
            center_x = int(points[:, 0].mean())
            center_y = int(points[:, 1].mean())

            # 中心に点を描画
            cv2.circle(
                frame,
                (center_x, center_y),
                5,
                (0, 0, 255),
                -1
            )

            # IDと中心座標を表示
            cv2.putText(
                frame,
                f"ID: {marker_id[0]}",
                (center_x + 10, center_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Center: ({center_x}, {center_y})",
                (center_x + 10, center_y + 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

            # ターミナルにも表示
            print(
                f"ID={marker_id[0]}, "
                f"Center=({center_x}, {center_y})"
            )

    # --------------------------------------
    # Display
    # --------------------------------------
    cv2.imshow("D435 Color + ArUco", frame)

    # qで終了
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()