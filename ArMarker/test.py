
import pyrealsense2 as rs
import traceback

pipeline = rs.pipeline()
config = rs.config()

# カラーとデプスの両方を有効化
config.enable_stream(
    rs.stream.color, 640, 480, rs.format.bgr8, 30
)
config.enable_stream(
    rs.stream.depth, 640, 480, rs.format.z16, 30
)

started = False

try:
    # ストリーミング開始
    profile = pipeline.start(config)
    started = True
    print("Pipeline started successfully")

    # フレーム取得
    frames = pipeline.wait_for_frames(timeout_ms=10000)
    print("Frameset:", type(frames))
    print("Number of frames:", frames.size())

    # デプスフレーム取得
    depth_frame = frames.get_depth_frame()
    print("Depth frame:", bool(depth_frame))

    # カラーフレーム取得
    try:
        color_frame = frames.get_color_frame()
        print("Color frame:", bool(color_frame))

    except Exception as e:
        print("Color exception:", type(e).__name__, str(e))
        traceback.print_exc()

    # フレームセット内の全フレームを確認
    for i, frame in enumerate(frames):
        p = frame.get_profile()
        print(
            f"Frame {i}: stream={p.stream_type()}, "
            f"format={p.format()}"
        )

except Exception as e:
    print("Pipeline exception:", type(e).__name__, str(e))
    traceback.print_exc()

finally:
    if started:
        pipeline.stop()
        print("Pipeline stopped")
