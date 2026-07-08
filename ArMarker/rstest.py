import pyrealsense2 as rs


# ==========================================
# カメラ情報を表示
# ==========================================
def print_camera_info(device):
    """接続されたRealSenseの情報を表示"""

    print("=" * 40)
    print("RealSense Device Information")
    print("=" * 40)
    print(f"Name             : {device.get_info(rs.camera_info.name)}")
    print(f"Serial Number    : {device.get_info(rs.camera_info.serial_number)}")
    print(f"Firmware Version : {device.get_info(rs.camera_info.firmware_version)}")
    print(f"Product Line     : {device.get_info(rs.camera_info.product_line)}")
    print(f"USB Type         : {device.get_info(rs.camera_info.usb_type_descriptor)}")
    print()


# ==========================================
# RGBカメラの有無を確認
# ==========================================
def has_rgb_sensor(device):
    """RGBカメラを搭載しているか確認"""

    for sensor in device.sensors:
        if sensor.get_info(rs.camera_info.name) == "RGB Camera":
            return True
    return False


# ==========================================
# メイン処理
# ==========================================
def main():

    # ------------------------------
    # RealSense初期化
    # ------------------------------
    pipeline = rs.pipeline()
    config = rs.config()

    try:
        # 接続デバイス取得
        pipeline_wrapper = rs.pipeline_wrapper(pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()

        # デバイス情報表示
        print_camera_info(device)

        # RGBカメラ確認
        if not has_rgb_sensor(device):
            print("RGB Camera が見つかりません。")
            return

        product_line = device.get_info(rs.camera_info.product_line)

        # ------------------------------
        # ストリーム設定
        # ------------------------------
        config.enable_stream(
            rs.stream.depth,
            640,
            480,
            rs.format.z16,
            30,
        )

        if product_line == "L500":
            config.enable_stream(
                rs.stream.color,
                960,
                540,
                rs.format.bgr8,
                30,
            )
        else:
            config.enable_stream(
                rs.stream.color,
                640,
                480,
                rs.format.bgr8,
                30,
            )

        # ------------------------------
        # ストリーミング開始
        # ------------------------------
        pipeline.start(config)
        print("RealSense camera connected.\n")

        # カメラを安定させる
        print("Warming up camera...")
        for _ in range(30):
            pipeline.wait_for_frames()

        # ------------------------------
        # フレーム取得
        # ------------------------------
        print("Capturing frame...")

        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if depth_frame and color_frame:
            print("Frame captured successfully.")
        else:
            print("Failed to capture frame.")

    except Exception as e:
        print(f"Error : {e}")

    finally:
        pipeline.stop()
        print("\nRealSense camera disconnected.")


# ==========================================
# エントリーポイント
# ==========================================
if __name__ == "__main__":
    main()