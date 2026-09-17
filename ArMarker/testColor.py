#カラーセンサーテストSDK不使用

import cv2

cap = cv2.VideoCapture("/dev/video4", cv2.CAP_V4L2)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

if not cap.isOpened():
    print("カメラを開けませんでした")
    exit()

print("カメラを開きました")

while True:
    ret, frame = cap.read()

    if not ret:
        print("フレームを取得できません")
        continue

    cv2.imshow("D435 Color", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()