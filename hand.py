from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD
import time

# ===============================
# 接続設定
# ===============================
mc = MyCobot(PI_PORT, 115200)
mc.power_off()
mc.power_on()

print("===== myCobot Pi =====")

print(mc.is_power_on())

if mc.is_power_on():
    print("電源ON")
else:
    print("電源ONに失敗しました。")
    exit()

time.sleep(2)

mc.send_angles([0, 0, 0, 0, 0, 0], 20)

time.sleep(2)

# ===============================
# 現在位置取得
# ===============================
origin = mc.get_coords()

if origin is None:
    print("現在位置を取得できませんでした。")
    exit()

print("\n現在位置")
print(f"X = {origin[0]:.1f} mm")
print(f"Y = {origin[1]:.1f} mm")
print(f"Z = {origin[2]:.1f} mm")

# ===============================
# 移動量入力
# ===============================
dx = float(input("\nX方向へ何cm移動しますか？ : "))
dy = float(input("Y方向へ何cm移動しますか？ : "))
dz = float(input("Z方向へ何cm移動しますか？ : "))

# cm → mm
dx *= 10
dy *= 10
dz *= 10

# ===============================
# 目標座標
# ===============================
target = origin.copy()

target[0] += dx
target[1] += dy
target[2] += dz

# ===============================
# 安全範囲（例）
# 必ず実機に合わせて変更してください
# ===============================
X_MIN = 100
X_MAX = 330

Y_MIN = -250
Y_MAX = 250

Z_MIN = 50
Z_MAX = 350

# ===============================
# 範囲チェック
# ===============================
if not (X_MIN <= target[0] <= X_MAX):
    print("X座標が安全範囲外です。")
    exit()

if not (Y_MIN <= target[1] <= Y_MAX):
    print("Y座標が安全範囲外です。")
    exit()

if not (Z_MIN <= target[2] <= Z_MAX):
    print("Z座標が安全範囲外です。")
    exit()

# ===============================
# 移動確認
# ===============================
print("\n===== 移動先 =====")
print(f"X = {target[0]:.1f}")
print(f"Y = {target[1]:.1f}")
print(f"Z = {target[2]:.1f}")

ans = input("\n移動しますか？ (y/n) : ")

if ans.lower() != "y":
    print("キャンセルしました。")
    exit()

# ===============================
# 移動
# 姿勢(Rx,Ry,Rz)は現在の姿勢を維持
# ===============================
mc.send_coords(target, 20, 0)

print("\n移動中...")

time.sleep(5)

# ===============================
# 移動後座標
# ===============================
current = mc.get_coords()

print("\n===== 移動後 =====")
print(f"X = {current[0]:.1f}")
print(f"Y = {current[1]:.1f}")
print(f"Z = {current[2]:.1f}")

print("\n完了しました。")