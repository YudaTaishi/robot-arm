"""
Raspberry Pi側: Windowsから送られたArUco座標をUDPで受信して表示する (動作確認用)
ここに カメラ座標系 -> ロボットベース座標系 の変換とロボット指令を組み込んでください。
"""
import json
import socket

LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))
print(f"Listening on UDP {LISTEN_PORT} ...")

while True:
    data, addr = sock.recvfrom(4096)
    try:
        msg = json.loads(data.decode("utf-8"))
    except json.JSONDecodeError:
        continue

    for m in msg["markers"]:
        x, y, z = m["xyz_m"]
        print(f"ID {m['id']}: pixel={m['pixel']}  X={x:+.3f} Y={y:+.3f} Z={z:+.3f} [m]")