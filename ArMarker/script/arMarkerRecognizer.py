import cv2

aruco = cv2.aruco

dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(dictionary, parameters)

cnt = 9

def recognizeArMarker():
    for i in range(cnt + 1):
        input_file_nm = f"ar{i}.png"
        output_file_nm = f"ar_detection{i}.png"

        input_img = cv2.imread(input_file_nm)

        corners, ids, rejected = detector.detectMarkers(input_img)

        ar_image = aruco.drawDetectedMarkers(input_img, corners, ids)

        cv2.imwrite(output_file_nm, ar_image)

if __name__ == "__main__":
    recognizeArMarker()