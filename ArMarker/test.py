import traceback

frames = pipeline.wait_for_frames()

depth_frame = frames.get_depth_frame()
print("Depth:", bool(depth_frame))

try:
    color_frame = frames.get_color_frame()
    print("Color:", bool(color_frame))

except Exception as e:
    print("Exception type:", type(e).__name__)
    print("Exception message:", str(e))
    traceback.print_exc()
    raise