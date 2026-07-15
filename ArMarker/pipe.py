profile = pipeline.start(config)

device = profile.get_device()
print(device.get_info(rs.camera_info.name))