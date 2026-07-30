import cv2
import numpy as np
import pyrealsense2 as rs
from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD

####################################################
# myCobot
####################################################
mc = MyCobot(PI_PORT, PI_BAUD)

####################################################
# RealSense
####################################################
pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

profile = pipeline.start(config)

align = rs.align(rs.stream.color)

intrinsics = profile.get_stream(
    rs.stream.color
).as_video_stream_profile().get_intrinsics()

####################################################
# ArUco
####################################################
aruco_dict = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_4X4_50
)

detector = cv2.aruco.ArucoDetector(
    aruco_dict,
    cv2.aruco.DetectorParameters()
)

####################################################
# HandEye
####################################################
# 例
R = np.eye(3)

t = np.array([
    [0.10],
    [0.02],
    [0.15]
])

####################################################
while True:

    frames = pipeline.wait_for_frames()

    frames = align.process(frames)

    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()

    if not color_frame or not depth_frame:
        continue

    color = np.asanyarray(color_frame.get_data())

    corners, ids, _ = detector.detectMarkers(color)

    if ids is not None:

        cv2.aruco.drawDetectedMarkers(color, corners, ids)

        c = corners[0][0]

        center_x = int(np.mean(c[:,0]))
        center_y = int(np.mean(c[:,1]))

        depth = depth_frame.get_distance(center_x, center_y)

        point = rs.rs2_deproject_pixel_to_point(
            intrinsics,
            [center_x, center_y],
            depth
        )

        camera_point = np.array(point).reshape(3,1)

        robot_point = R @ camera_point + t

        x = robot_point[0,0] * 1000
        y = robot_point[1,0] * 1000
        z = robot_point[2,0] * 1000

        print("--------------------------------")
        print("Camera")
        print(camera_point)

        print("Robot")
        print(robot_point)

        cv2.circle(color, (center_x, center_y), 5, (0,0,255), -1)

        ####################################################
        # ロボット移動
        ####################################################
        rx = 180
        ry = 0
        rz = 0

        mc.send_coords(
            [x, y, z, rx, ry, rz],
            30,
            1
        )

    cv2.imshow("RealSense", color)

    key = cv2.waitKey(1)

    if key == 27:
        break

pipeline.stop()
cv2.destroyAllWindows()